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

    /**
     * Gets available courses
     *
     * @throws ScheduleNotFoundException throws when schedule not found
     * @throws RuntimeException throws when schedule do not have a courses
     * @return list of available courses
     */
    fun getAvailableCourses(): List<Int>

    /**
     * Gets available programs for this course
     *
     * @param course user's course
     * @throws ScheduleNotFoundException throws when schedule not found
     * @throws IllegalArgumentException throws when user's course not found in schedule
     * @return list of available programs
     */
    fun getAvailablePrograms(course: Int): List<String>

    /**
     * Gets available groups for this program and course
     *
     * @param course user's course
     * @param program user's program
     * @throws ScheduleNotFoundException throws when schedule not found
     * @throws IllegalArgumentException throws when user's program not found in schedule
     * @return list of available groups
     */
    fun getAvailableGroups(course: Int, program: String): List<String>

    /**
     * Gets available subgroups for this group, course and program
     *
     * @param course user's course
     * @param program user's program
     * @param group user's group
     * @throws ScheduleNotFoundException throws when schedule not found
     * @throws IllegalArgumentException throws when user's group not found in schedule
     * @throws RuntimeException throws when catching error in subgroup parsing
     * @return list of available subgroups for this group
     */
    fun getAvailableSubgroups(course: Int, program: String, group: String): List<Int>
}