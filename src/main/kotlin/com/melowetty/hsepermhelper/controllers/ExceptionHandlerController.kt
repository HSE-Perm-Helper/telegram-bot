package com.melowetty.hsepermhelper.controllers

import com.melowetty.hsepermhelper.exceptions.*
import com.melowetty.hsepermhelper.models.ErrorResponse
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.http.converter.HttpMessageNotReadableException
import org.springframework.web.bind.MissingServletRequestParameterException
import org.springframework.web.bind.annotation.ExceptionHandler
import org.springframework.web.bind.annotation.RestControllerAdvice
import org.springframework.web.servlet.NoHandlerFoundException

@RestControllerAdvice
class ExceptionHandlerController {
    @ExceptionHandler(ScheduleNotFoundException::class)
    fun handleScheduleNotFoundException(exception: ScheduleNotFoundException): ResponseEntity<ErrorResponse> {
        return exception.toResponseEntity()
    }

    @ExceptionHandler(RuntimeException::class)
    fun handleRuntimeException(exception: java.lang.RuntimeException): ResponseEntity<ErrorResponse> {
        val response = exception.message?.let { ErrorResponse(message = it, code = exception.javaClass.simpleName, status = HttpStatus.INTERNAL_SERVER_ERROR.value()) }
        return ResponseEntity<ErrorResponse>(response, HttpStatus.INTERNAL_SERVER_ERROR)
    }

    @ExceptionHandler(NoHandlerFoundException::class)
    fun handleNoHandlerFoundException(exception: NoHandlerFoundException): ResponseEntity<ErrorResponse> {
        val response = ErrorResponse(
            message = "Страница не найдена!",
            code = exception.javaClass.simpleName,
            status = HttpStatus.NOT_FOUND.value()
        )
        return ResponseEntity<ErrorResponse>(response, HttpStatus.NOT_FOUND)
    }

    @ExceptionHandler(UserNotFoundException::class)
    fun handleUserNotFoundException(exception: UserNotFoundException): ResponseEntity<ErrorResponse> {
        return exception.toResponseEntity()
    }

    @ExceptionHandler(PermissionDeniedException::class)
    fun handlePermissionDeniedException(exception: PermissionDeniedException): ResponseEntity<ErrorResponse> {
        return exception.toResponseEntity()
    }

    @ExceptionHandler(UnauthorizedException::class)
    fun handleUnauthorizedException(exception: UnauthorizedException): ResponseEntity<ErrorResponse> {
        return exception.toResponseEntity()
    }

    @ExceptionHandler(SecretKeyParseException::class)
    fun handleSecretKeyParseException(exception: SecretKeyParseException): ResponseEntity<ErrorResponse> {
        return exception.toResponseEntity()
    }

    @ExceptionHandler(MissingServletRequestParameterException::class)
    fun handleSecretKeyParseException(exception: MissingServletRequestParameterException): ResponseEntity<ErrorResponse> {
        val response = ErrorResponse(
            message = "Необходимый параметр запроса ${exception.parameterName} типа ${exception.parameterType} не передан!",
            code = exception.javaClass.simpleName,
            status = HttpStatus.BAD_REQUEST.value()
        )
        return ResponseEntity<ErrorResponse>(response, HttpStatus.BAD_REQUEST)
    }

    @ExceptionHandler(HttpMessageNotReadableException::class)
    fun handleSecretKeyParseException(exception: HttpMessageNotReadableException): ResponseEntity<ErrorResponse> {
        val response = ErrorResponse(
            message = "Необходимое тело запроса не передано!",
            code = exception.javaClass.simpleName,
            status = HttpStatus.BAD_REQUEST.value()
        )
        return ResponseEntity<ErrorResponse>(response, HttpStatus.BAD_REQUEST)
    }

    @ExceptionHandler(IllegalArgumentException::class)
    fun handleIllegalArgumentException(exception: IllegalArgumentException): ResponseEntity<ErrorResponse> {
        val response = ErrorResponse(
            message = exception.message ?: "Неверный параметр в запросе!",
            code = exception.javaClass.simpleName,
            status = HttpStatus.BAD_REQUEST.value()
        )
        return ResponseEntity<ErrorResponse>(response, HttpStatus.BAD_REQUEST)
    }
}