package com.melowetty.hsepermhelper.exceptions

import org.springframework.http.HttpStatus

class SecretKeyParseException(message: String): CustomException(message, HttpStatus.INTERNAL_SERVER_ERROR)