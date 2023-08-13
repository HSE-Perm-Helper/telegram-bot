package com.melowetty.hsepermhelper.service

import Schedule
import com.melowetty.hsepermhelper.models.ScheduleFile
import org.springframework.core.io.Resource
import java.util.*

interface ScheduleService {
    fun getCurrentSchedule(telegramId: Long): Schedule

    fun getCurrentSchedule(id: UUID): Schedule

    fun getNextSchedule(telegramId: Long): Schedule

    fun getNextSchedule(id: UUID): Schedule

    /**
     * Returns resource file for mobile calendar of schedule for user
     * @param id user's id
     * @return resource .ics file
     */
    fun getScheduleResource(id: UUID): Resource

    /**
     * Returns links for mobile calendar of schedule for user
     * @param id user's telegram id
     * @return schedule file object
     */
    fun getScheduleFileByTelegramId(id: Long): ScheduleFile

    fun getAvailableCourses(): List<Int>

    fun getAvailablePrograms(course: Int): List<String>

    fun getAvailableGroups(course: Int, program: String): List<String>

    fun getAvailableSubgroups(course: Int, program: String, group: String): List<Int>

    /**
     * Refresh schedule files for users
     *
     */
    fun refreshScheduleFiles()
}