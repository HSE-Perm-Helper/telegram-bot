package com.melowetty.hsepermhelper.service

import Schedule

interface ScheduleService {
    fun getCurrentSchedule(telegramId: Long): Schedule
    fun getNextSchedule(telegramId: Long): Schedule
}