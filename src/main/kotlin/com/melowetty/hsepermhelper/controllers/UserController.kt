package com.melowetty.hsepermhelper.controllers

import com.melowetty.hsepermhelper.dto.UserDto
import com.melowetty.hsepermhelper.models.Response
import com.melowetty.hsepermhelper.service.UserService
import io.swagger.v3.oas.annotations.Operation
import io.swagger.v3.oas.annotations.Parameter
import io.swagger.v3.oas.annotations.security.SecurityRequirement
import io.swagger.v3.oas.annotations.tags.Tag
import org.springframework.http.MediaType
import org.springframework.web.bind.annotation.*
import java.util.UUID

@Tag(name = "Пользователи", description = "Взаимодействие с пользователями")
@RestController
@RequestMapping("users")
class UserController(
    private val userService: UserService
) {
    @SecurityRequirement(name = "X-Secret-Key")
    @Operation(
        summary = "Получение пользователя по Telegram ID",
        description = "Позволяет получить пользователя по его Telegram ID"
    )
    @GetMapping(
        produces = [MediaType.APPLICATION_JSON_VALUE]
    )
    fun getUserByTelegramId(
        @Parameter(description = "Telegram ID пользователя")
        @RequestParam("telegramId")
        telegramId: Long,
    ): Response<UserDto> {
        return Response(userService.getByTelegramId(telegramId = telegramId))
    }

    @SecurityRequirement(name = "X-Secret-Key")
    @Operation(
        summary = "Получение пользователя",
        description = "Позволяет получить пользователя по его ID"
    )
    @GetMapping(
        "/{id}",
        produces = [MediaType.APPLICATION_JSON_VALUE]
    )
    fun getUserById(
        @Parameter(description = "ID пользователя")
        @PathVariable("id")
        id: UUID,
    ): Response<UserDto> {
        return Response(userService.getById(id))
    }

    @SecurityRequirement(name = "X-Secret-Key")
    @Operation(
        summary = "Регистрация пользователя",
        description = "Позволяет зарегистрировать пользователя"
    )
    @PostMapping(
        consumes = [MediaType.APPLICATION_JSON_VALUE],
        produces = [MediaType.APPLICATION_JSON_VALUE])
    fun createUser(
        @RequestBody userDto: UserDto,
    ): Response<UserDto> {
        val user = userService.create(dto = userDto)
        return Response(user)
    }
}