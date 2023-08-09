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

    @SecurityRequirement(name = "X-Secret-Key")
    @Operation(
        summary = "Получение доступных для выбора курсов",
        description = "Позволяет получить доступные для выбора курсы для регистрации"
    )
    @GetMapping(
        "schedule/available_courses"
    )
    fun getAvailableCourses(
    ): Response {
        return Response(scheduleService.getAvailableCourses())
    }

    @SecurityRequirement(name = "X-Secret-Key")
    @Operation(
        summary = "Получение доступных для выбора проргамм",
        description = "Позволяет получить доступные для выбора программ для регистрации"
    )
    @GetMapping(
        "schedule/available_programs"
    )
    fun getAvailablePrograms(
        @Parameter(description = "Номер курса")
        @RequestParam("course")
        course: Int,
    ): Response {
        return Response(scheduleService.getAvailablePrograms(course))
    }

    @SecurityRequirement(name = "X-Secret-Key")
    @Operation(
        summary = "Получение доступных для выбора групп",
        description = "Позволяет получить доступные для выбора группы для регистрации"
    )
    @GetMapping(
        "schedule/available_groups"
    )
    fun getAvailableGroups(
        @Parameter(description = "Номер курса")
        @RequestParam("course")
        course: Int,
        @Parameter(description = "Образовательная программа")
        @RequestParam("program")
        program: String,
    ): Response {
        return Response(scheduleService.getAvailableGroups(course, program))
    }

    @SecurityRequirement(name = "X-Secret-Key")
    @Operation(
        summary = "Получение доступных для выбора подгрупп",
        description = "Позволяет получить доступные для выбора подгруппы для регистрации"
    )
    @GetMapping(
        "schedule/available_subgroups"
    )
    fun getAvailableSubgroups(
        @Parameter(description = "Номер курса")
        @RequestParam("course")
        course: Int,
        @Parameter(description = "Образовательная программа")
        @RequestParam("program")
        program: String,
        @Parameter(description = "Группа студента")
        @RequestParam("group")
        group: String
    ): Response {
        return Response(scheduleService.getAvailableSubgroups(course, program, group))
    }

}