package com.melowetty.hsepermhelper.exceptions

import org.springframework.http.HttpStatus

class UserIsExistsException(message: String): CustomException(message, HttpStatus.CONFLICT)