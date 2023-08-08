package com.melowetty.hsepermhelper.service.impl

import com.melowetty.hsepermhelper.dto.UserDto
import com.melowetty.hsepermhelper.entity.UserEntity
import com.melowetty.hsepermhelper.exceptions.UserNotFoundException
import com.melowetty.hsepermhelper.repository.UserRepository
import com.melowetty.hsepermhelper.service.UserService
import org.springframework.stereotype.Service

@Service
class UserServiceImpl(
    private val userRepository: UserRepository
): UserService {
    override fun getByTelegramId(telegramId: Long): UserDto {
        val user = userRepository.findByTelegramId(telegramId)
        if(user.isEmpty) throw UserNotFoundException("Пользователь с таким Telegram ID не найден!")
        return user.get().toDto()
    }

    override fun create(dto: UserDto): Long {
        return userRepository.save(dto.toEntity()).telegramId
    }

    fun UserEntity.toDto(): UserDto {
        return UserDto(
            telegramId = telegramId,
            settings = settings,
        )
    }

    fun UserDto.toEntity(): UserEntity {
        return UserEntity(
            id = 0,
            telegramId = telegramId,
            settings = settings,
        )
    }
}