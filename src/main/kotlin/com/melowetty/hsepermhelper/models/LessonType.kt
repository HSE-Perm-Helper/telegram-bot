package com.melowetty.hsepermhelper.models

enum class LessonType(val type: String, val pattern: String) {
    LECTURE("Лекция", "{type}: {subject}"),
    SEMINAR("Семинар", "{type}: {subject}"),
    EXAM("Экзамен", "{type}: {subject}"),
    PRACTICE("Практика", "{type}: {subject}"),
    MINOR("Майнор", "{type}"),
    ENGLISH("Английский", "{type}"),
    STATEMENT("Ведомость", "{type}: {subject}"),
    ICC("МКД", "{type}: {subject}");
    fun toEventSubject(subject: String): String {
        return pattern
            .replace("{type}", type)
            .replace("{subject}", subject)
    }
}