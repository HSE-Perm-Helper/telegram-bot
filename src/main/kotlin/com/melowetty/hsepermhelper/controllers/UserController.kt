package com.melowetty.hsepermhelper.controllers

import com.melowetty.hsepermhelper.dto.UserDto
import com.melowetty.hsepermhelper.models.Response
import com.melowetty.hsepermhelper.service.UserService
import io.swagger.v3.oas.annotations.Operation
import io.swagger.v3.oas.annotations.Parameter
import io.swagger.v3.oas.annotations.security.SecurityRequirement
import io.swagger.v3.oas.annotations.tags.Tag
import org.springframework.web.bind.annotation.*

@Tag(name = "Пользователи", description = "Взаимодействие с пользователями")
@RestController
@RequestMapping("users")
class UserController(
    private val userService: UserService
) {
    @SecurityRequirement(name = "X-Secret-Key")
    @Operation(
        summary = "Получение пользователя",
        description = "Позволяет получить пользователя по его Telegram ID"
    )
    @GetMapping
    fun getUserByTelegramId(
        @Parameter(description = "Telegram ID пользователя")
        @RequestParam("telegramId")
        telegramId: Long,
    ): Response {
        return Response(userService.getByTelegramId(telegramId = telegramId))
    }

    @SecurityRequirement(name = "X-Secret-Key")
    @Operation(
        summary = "Регистрация пользователя",
        description = "Позволяет зарегистрировать пользователя"
    )
    @PostMapping
    fun createUser(
        @RequestBody userDto: UserDto,
    ): Response {
        val id = userService.create(dto = userDto)
        return Response(mapOf("id" to id))
    }
}