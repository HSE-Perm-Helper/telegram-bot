package com.melowetty.hsepermhelper.entity

import com.melowetty.hsepermhelper.models.Settings
import jakarta.persistence.*

@Entity
@Table(name = "users")
data class UserEntity(
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    val id: Long = 0L,

    @Column(name = "telegram_id")
    val telegramId: Long = 0L,

    val settings: Settings? = null,
)