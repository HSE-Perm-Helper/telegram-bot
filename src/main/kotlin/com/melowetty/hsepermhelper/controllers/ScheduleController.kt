package com.melowetty.hsepermhelper.controllers

import com.melowetty.hsepermhelper.models.Response
import com.melowetty.hsepermhelper.service.ScheduleService
import io.swagger.v3.oas.annotations.Operation
import io.swagger.v3.oas.annotations.Parameter
import io.swagger.v3.oas.annotations.security.SecurityRequirement
import io.swagger.v3.oas.annotations.tags.Tag
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController

@Tag(name = "Расписание", description = "Взаимодействие с расписанием")
@RestController
class ScheduleController(
    private val scheduleService: ScheduleService
) {

    @SecurityRequirement(name = "X-Secret-Key")
    @Operation(
        summary = "Получение расписания текущей недели",
        description = "Позволяет получить расписания текущей недели для пользователя по его Telegram ID"
    )
    @GetMapping(
        "current_schedule"
    )
    fun getCurrentSchedule(
        @Parameter(description = "Telegram ID пользователя")
        @RequestParam("telegramId")
        telegramId: Long,
    ): Response {
        return Response(scheduleService.getCurrentSchedule(telegramId))
    }

    @SecurityRequirement(name = "X-Secret-Key")
    @Operation(
        summary = "Получение расписания следующей недели",
        description = "Позволяет получить расписания следующей недели для пользователя по его Telegram ID"
    )
    @GetMapping(
        "next_schedule",
    )
    fun getNextSchedule(
        @Parameter(description = "Telegram ID пользователя")
        @RequestParam("telegramId")
        telegramId: Long,
    ): Response {
        return Response(scheduleService.getNextSchedule(telegramId))
    }

}