package com.melowetty.hsepermhelper.models

import Lesson
import com.fasterxml.jackson.annotation.JsonFormat
import com.fasterxml.jackson.annotation.JsonIgnore
import com.fasterxml.jackson.annotation.JsonKey
import com.melowetty.hsepermhelper.utils.DateUtils
import java.time.LocalDate

data class LessonDay(
    @JsonFormat(pattern = DateUtils.DATE_PATTERN)
    @JsonKey
    val date: LocalDate,

    @JsonIgnore
    val lessons: List<Lesson>
)
