package com.melowetty.hsepermhelper.service

import Schedule

interface ScheduleService {
    fun getCurrentSchedule(telegramId: Long): Schedule

    fun getNextSchedule(telegramId: Long): Schedule

    fun getAvailableCourses(): List<Int>

    fun getAvailablePrograms(course: Int): List<String>

    fun getAvailableGroups(course: Int, program: String): List<String>

    fun getAvailableSubgroups(course: Int, program: String, group: String): List<Int>
}