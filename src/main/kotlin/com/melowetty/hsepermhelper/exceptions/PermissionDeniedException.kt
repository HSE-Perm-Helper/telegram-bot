package com.melowetty.hsepermhelper.exceptions

import org.springframework.http.HttpStatus

class PermissionDeniedException(message: String): CustomException(message, HttpStatus.FORBIDDEN)