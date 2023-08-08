package com.melowetty.hsepermhelper.repository

import Schedule

interface ScheduleRepository {
    /**
     * Gets this week schedule and return null when schedule is not found/checking through error
     * @return this week schedule or null if schedule not found
     */
    fun getCurrentSchedule(): Schedule?

    /**
     * Gets next week schedule and return null when schedule is not found/checking through error
     * @return next week schedule or null if schedule not found
     */
    fun getNextSchedule(): Schedule?
}