package com.melowetty.hsepermhelper.models

import io.swagger.v3.oas.annotations.media.Schema
import jakarta.persistence.Column
import jakarta.persistence.Embeddable

@Schema(description = "Настройки пользователя")
@Embeddable
data class Settings(
    @Schema(description = "Учебная группа пользователя", example = "РИС-22-3")
    @Column(name = "user_group")
    val group: String = "",

    @Schema(description = "Учебная подгруппа пользователя", example = "5")
    @Column(name = "user_sub_group")
    val subGroup: Int = 0,
)
