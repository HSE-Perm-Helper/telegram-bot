package com.melowetty.hsepermhelper.dto

import com.melowetty.hsepermhelper.models.Settings
import io.swagger.v3.oas.annotations.media.Schema

@Schema(name = "User")
data class UserDto(
    @Schema(description = "Telegram ID пользователя", example = "123432412")
    val telegramId: Long = 0L,
    @Schema(description = "Настройки пользователя")
    val settings: Settings? = null,
)