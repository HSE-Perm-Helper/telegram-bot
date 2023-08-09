package com.melowetty.hsepermhelper.service.impl

import Lesson
import Schedule
import com.melowetty.hsepermhelper.dto.UserDto
import com.melowetty.hsepermhelper.exceptions.ScheduleNotFoundException
import com.melowetty.hsepermhelper.repository.ScheduleRepository
import com.melowetty.hsepermhelper.service.ScheduleService
import com.melowetty.hsepermhelper.service.UserService
import org.springframework.stereotype.Service

@Service
class ScheduleServiceImpl(
    private val scheduleRepository: ScheduleRepository,
    private val userService: UserService,
): ScheduleService {
    private fun filterSchedule(schedule: Schedule, user: UserDto): Schedule {
        val filteredLessons = schedule.lessons.flatMap { it.value }.filter{ lesson: Lesson ->
            if (lesson.subGroup != null) lesson.group == user.settings?.group
                    && lesson.subGroup == user.settings.subGroup
            else lesson.group == user.settings?.group
        }
        val groupedLessons = filteredLessons.groupBy { it.date }
        return schedule.copy(
            lessons = groupedLessons
        )
    }

    override fun getCurrentSchedule(telegramId: Long): Schedule {
        val user = userService.getByTelegramId(telegramId)
        val schedule = scheduleRepository.getCurrentSchedule() ?: throw ScheduleNotFoundException("Расписание на текущую неделю не было найдено!")
        return filterSchedule(schedule, user)
    }

    override fun getNextSchedule(telegramId: Long): Schedule {
        val user = userService.getByTelegramId(telegramId)
        val schedule = scheduleRepository.getNextSchedule() ?: throw ScheduleNotFoundException("Расписание на следующую неделю не было найдено!")
        return filterSchedule(schedule, user)
    }

    override fun getAvailableCourses(): List<Int> {
        return scheduleRepository.getAvailableCourses()
    }

    override fun getAvailablePrograms(course: Int): List<String> {
        return scheduleRepository.getAvailablePrograms(course = course)
    }

    override fun getAvailableGroups(course: Int, program: String): List<String> {
        return scheduleRepository.getAvailableGroups(course = course, program = program)
    }

    override fun getAvailableSubgroups(course: Int, program: String, group: String): List<Int> {
        return scheduleRepository.getAvailableSubgroups(course = course, program = program, group = group)
    }


}