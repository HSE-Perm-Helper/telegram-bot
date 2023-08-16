package com.melowetty.hsepermhelper.events

open class CustomEvent<T>(
    val source: T,
    val type: EventType
)