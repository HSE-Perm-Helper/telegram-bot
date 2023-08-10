package com.melowetty.hsepermhelper.controllers

import Schedule
import com.melowetty.hsepermhelper.models.Response
import com.melowetty.hsepermhelper.service.ScheduleService
import io.swagger.v3.oas.annotations.Operation
import io.swagger.v3.oas.annotations.Parameter
import io.swagger.v3.oas.annotations.security.SecurityRequirement
import io.swagger.v3.oas.annotations.tags.Tag
import org.springframework.aot.hint.predicate.RuntimeHintsPredicates.resource
import org.springframework.core.io.Resource
import org.springframework.http.HttpHeaders
import org.springframework.http.MediaType
import org.springframework.http.ResponseEntity
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
        "current_schedule",
        produces = [MediaType.APPLICATION_JSON_VALUE]
    )
    fun getCurrentSchedule(
        @Parameter(description = "Telegram ID пользователя")
        @RequestParam("telegramId")
        telegramId: Long,
    ): Response<Schedule> {
        return Response(scheduleService.getCurrentSchedule(telegramId))
    }

    @SecurityRequirement(name = "X-Secret-Key")
    @Operation(
        summary = "Получение расписания текущей недели в виде файла",
        description = "Позволяет получить расписания текущей недели в виде файла для пользователя по его Telegram ID"
    )
    @GetMapping(
        "current_schedule/download",
        produces = [MediaType.APPLICATION_OCTET_STREAM_VALUE]
    )
    fun getCurrentScheduleFile(
        @Parameter(description = "Telegram ID пользователя")
        @RequestParam("telegramId")
        telegramId: Long,
    ): ResponseEntity<Resource> {
        val resource = scheduleService.getCurrentScheduleFile(telegramId)
        return getFileDownloadResponse(resource)
    }

    @SecurityRequirement(name = "X-Secret-Key")
    @Operation(
        summary = "Получение расписания следующей недели",
        description = "Позволяет получить расписания следующей недели для пользователя по его Telegram ID"
    )
    @GetMapping(
        "next_schedule",
        produces = [MediaType.APPLICATION_JSON_VALUE]
    )
    fun getNextSchedule(
        @Parameter(description = "Telegram ID пользователя")
        @RequestParam("telegramId")
        telegramId: Long,
    ): Response<Schedule> {
        return Response(scheduleService.getNextSchedule(telegramId))
    }

    @SecurityRequirement(name = "X-Secret-Key")
    @Operation(
        summary = "Получение расписания следующей недели в виде файла",
        description = "Позволяет получить расписания следующей недели в виде файла для пользователя по его Telegram ID"
    )
    @GetMapping(
        "current_schedule/download",
        produces = [MediaType.APPLICATION_OCTET_STREAM_VALUE]
    )
    fun getNextScheduleFile(
        @Parameter(description = "Telegram ID пользователя")
        @RequestParam("telegramId")
        telegramId: Long,
    ): ResponseEntity<Resource> {
        val resource = scheduleService.getNextScheduleFile(telegramId)
        return getFileDownloadResponse(resource)
    }

    @SecurityRequirement(name = "X-Secret-Key")
    @Operation(
        summary = "Получение доступных для выбора курсов",
        description = "Позволяет получить доступные для выбора курсы для регистрации"
    )
    @GetMapping(
        "schedule/available_courses",
        produces = [MediaType.APPLICATION_JSON_VALUE]
    )
    fun getAvailableCourses(
    ): Response<List<Int>> {
        return Response(scheduleService.getAvailableCourses())
    }

    @SecurityRequirement(name = "X-Secret-Key")
    @Operation(
        summary = "Получение доступных для выбора проргамм",
        description = "Позволяет получить доступные для выбора программ для регистрации",
    )
    @GetMapping(
        "schedule/available_programs",
        produces = [MediaType.APPLICATION_JSON_VALUE]
    )
    fun getAvailablePrograms(
        @Parameter(description = "Номер курса")
        @RequestParam("course")
        course: Int,
    ): Response<List<String>> {
        return Response(scheduleService.getAvailablePrograms(course))
    }

    @SecurityRequirement(name = "X-Secret-Key")
    @Operation(
        summary = "Получение доступных для выбора групп",
        description = "Позволяет получить доступные для выбора группы для регистрации",
    )
    @GetMapping(
        "schedule/available_groups",
        produces = [MediaType.APPLICATION_JSON_VALUE]
    )
    fun getAvailableGroups(
        @Parameter(description = "Номер курса")
        @RequestParam("course")
        course: Int,
        @Parameter(description = "Образовательная программа")
        @RequestParam("program")
        program: String,
    ): Response<List<String>> {
        return Response(scheduleService.getAvailableGroups(course, program))
    }

    @SecurityRequirement(name = "X-Secret-Key")
    @Operation(
        summary = "Получение доступных для выбора подгрупп",
        description = "Позволяет получить доступные для выбора подгруппы для регистрации"
    )
    @GetMapping(
        "schedule/available_subgroups",
        produces = [MediaType.APPLICATION_JSON_VALUE]
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
    ): Response<List<Int>> {
        return Response(scheduleService.getAvailableSubgroups(course, program, group))
    }

    private fun getFileDownloadResponse(resource: Resource): ResponseEntity<Resource> {
        val header = HttpHeaders()
        header.add(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=schedule.ics")
        header.add("Cache-Control", "no-cache, no-store, must-revalidate")
        header.add("Pragma", "no-cache")
        header.add("Expires", "0")

        return ResponseEntity
            .ok()
            .headers(header)
            .contentType(MediaType.APPLICATION_OCTET_STREAM)
            .body(resource)
    }

}