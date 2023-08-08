package com.melowetty.hsepermhelper.exceptions

import org.springframework.http.HttpStatus

class UnauthorizedException(message: String): CustomException(message, HttpStatus.UNAUTHORIZED)