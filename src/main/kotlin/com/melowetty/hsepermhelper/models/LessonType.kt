package com.melowetty.hsepermhelper.models

enum class LessonType(val type: String, private val scheduleFilePattern: String) {
    LECTURE("Лекция", "{type}: {subject}"),
    SEMINAR("Семинар", "{type}: {subject}"),
    EXAM("Экзамен", "{type}: {subject}") {
        override fun reformatSubject(subject: String): String {
            return subject.replace("ЭКЗАМЕН", "").trim()
        }
    },
    TEST("Зачёт", "{type}: {subject}") {
        override fun reformatSubject(subject: String): String {
            return subject.replace("ЗАЧЕТ", "").trim()
        }
    },
    PRACTICE("Практика", "{type}: {subject}") {
        override fun reformatSubject(subject: String): String {
            return if (subject == "ПРАКТИКА") ""
            else subject
        }
    },
    MINOR("Майнор", "{type}"),
    ENGLISH("Английский", "{type}"),
    STATEMENT("Ведомость", "{type}: {subject}"),
    ICC("МКД", "{type}: {subject}");
    fun toEventSubject(subject: String): String {
        return scheduleFilePattern
            .replace("{type}", type)
            .replace("{subject}", subject)
    }
    public open fun reformatSubject(subject: String): String {
        return subject
    }
}