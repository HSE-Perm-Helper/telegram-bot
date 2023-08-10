package com.melowetty.hsepermhelper.service

import Schedule
import org.springframework.core.io.Resource

interface ScheduleService {
    fun getCurrentSchedule(telegramId: Long): Schedule

    fun getNextSchedule(telegramId: Long): Schedule

    /**
     * Returns resource file for phone calendar of current schedule for user
     * @param telegramId user's telegram id
     * @return resource .ics file
     */
    fun getCurrentScheduleFile(telegramId: Long): Resource

    /**
     * Returns resource file for phone calendar of next schedule for user
     * @param telegramId user's telegram id
     * @return resource .ics file
     */
    fun getNextScheduleFile(telegramId: Long): Resource

    fun getAvailableCourses(): List<Int>

    fun getAvailablePrograms(course: Int): List<String>

    fun getAvailableGroups(course: Int, program: String): List<String>

    fun getAvailableSubgroups(course: Int, program: String, group: String): List<Int>
}