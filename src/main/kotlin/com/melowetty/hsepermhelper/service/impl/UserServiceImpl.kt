package com.melowetty.hsepermhelper.service.impl

import com.melowetty.hsepermhelper.dto.UserDto
import com.melowetty.hsepermhelper.entity.UserEntity
import com.melowetty.hsepermhelper.exceptions.UserNotFoundException
import com.melowetty.hsepermhelper.repository.UserRepository
import com.melowetty.hsepermhelper.service.UserService
import org.springframework.stereotype.Service
import java.util.*

@Service
class UserServiceImpl(
    private val userRepository: UserRepository
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
        return userRepository.save(dto.toEntity()).toDto()
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