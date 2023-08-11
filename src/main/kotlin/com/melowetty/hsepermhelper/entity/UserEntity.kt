package com.melowetty.hsepermhelper.entity

import com.melowetty.hsepermhelper.models.Settings
import jakarta.persistence.*
import java.util.UUID

@Entity
@Table(name = "users")
data class UserEntity(
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    val id: UUID = UUID.randomUUID(),

    @Column(name = "telegram_id")
    val telegramId: Long = 0L,

    val settings: Settings? = null,
)