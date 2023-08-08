package com.melowetty.hsepermhelper.repository

import com.melowetty.hsepermhelper.entity.UserEntity
import org.springframework.data.repository.CrudRepository
import org.springframework.stereotype.Repository
import java.util.*

@Repository
interface UserRepository: CrudRepository<UserEntity, Long> {
    fun findByTelegramId(telegramId: Long): Optional<UserEntity>
}