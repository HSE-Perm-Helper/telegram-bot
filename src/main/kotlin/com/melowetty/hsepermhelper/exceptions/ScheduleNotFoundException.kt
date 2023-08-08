package com.melowetty.hsepermhelper.exceptions

import org.springframework.http.HttpStatus

class ScheduleNotFoundException(message: String) : CustomException(message, HttpStatus.NOT_FOUND)