package com.melowetty.hsepermhelper.service.impl

import com.melowetty.hsepermhelper.dto.UserDto
import com.melowetty.hsepermhelper.entity.UserEntity
import com.melowetty.hsepermhelper.events.EventType
import com.melowetty.hsepermhelper.events.UsersChangedEvent
import com.melowetty.hsepermhelper.exceptions.UserIsExistsException
import com.melowetty.hsepermhelper.exceptions.UserNotFoundException
import com.melowetty.hsepermhelper.repository.UserRepository
import com.melowetty.hsepermhelper.service.UserService
import org.springframework.context.ApplicationEventPublisher
import org.springframework.stereotype.Service
import java.util.*

@Service
class UserServiceImpl(
    private val eventPublisher: ApplicationEventPublisher,
    private val userRepository: UserRepository,
): UserService {
    override fun getByTelegramId(telegramId: Long): UserDto {
        val user = userRepository.findByTelegramId(telegramId)
        if(user.isEmpty) throw UserNotFoundException("Пользователь с таким Telegram ID не найден!")
        return user.get().toDto()
    }

    override fun getById(id: UUID): UserDto {
        val user = userRepository.findById(id)
        if(user.isEmpty) throw UserNotFoundException("Пользователь с таким ID не найден!")
        return user.get().toDto()
    }

    override fun create(dto: UserDto): UserDto {
        val isExists = userRepository.existsByTelegramId(dto.telegramId)
        if(isExists) throw UserIsExistsException("Пользователь с таким Telegram ID уже существует!")
        val user = userRepository.save(dto.toEntity()).toDto()
        val event = UsersChangedEvent(
            user = user,
            type = EventType.ADDED
        )
        eventPublisher.publishEvent(event)
        return user
    }

    override fun deleteById(id: UUID) {
        val user = userRepository.findById(id)
        if (user.isEmpty) throw UserNotFoundException("Пользователь с таким ID не найден!")
        userRepository.delete(user.get())
        val event = UsersChangedEvent(
            user = user.get().toDto(),
            type = EventType.DELETED
        )
        eventPublisher.publishEvent(event)
    }

    override fun deleteByTelegramId(telegramId: Long) {
        val user = userRepository.findByTelegramId(telegramId)
        if (user.isEmpty) throw UserNotFoundException("Пользователь с таким Telegram ID не найден!")
        userRepository.delete(user.get())
        val event = UsersChangedEvent(
            user = user.get().toDto(),
            type = EventType.DELETED
        )
        eventPublisher.publishEvent(event)
    }

    override fun getAllUsers(): List<UserDto> {
        return userRepository.findAll().map { it.toDto() }
    }

    fun UserEntity.toDto(): UserDto {
        return UserDto(
            id = id,
            telegramId = telegramId,
            settings = settings,
        )
    }

    fun UserDto.toEntity(): UserEntity {
        return UserEntity(
            id = UUID.randomUUID(),
            telegramId = telegramId,
            settings = settings,
        )
    }
}