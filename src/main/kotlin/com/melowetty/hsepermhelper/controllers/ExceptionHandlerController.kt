package com.melowetty.hsepermhelper.controllers

import com.melowetty.hsepermhelper.exceptions.*
import com.melowetty.hsepermhelper.models.ErrorResponse
import org.springframework.core.env.Environment
import org.springframework.core.env.get
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.http.converter.HttpMessageNotReadableException
import org.springframework.web.bind.MissingServletRequestParameterException
import org.springframework.web.bind.annotation.ExceptionHandler
import org.springframework.web.bind.annotation.ResponseStatus
import org.springframework.web.bind.annotation.RestControllerAdvice
import org.springframework.web.servlet.NoHandlerFoundException
import java.io.FileNotFoundException
import java.lang.Boolean.parseBoolean

@RestControllerAdvice
class ExceptionHandlerController(
    environment: Environment
) {
    val isDebug = parseBoolean(environment["app.debug.enable"])
    @ResponseStatus(HttpStatus.NOT_FOUND)
    @ExceptionHandler(ScheduleNotFoundException::class)
    fun handleScheduleNotFoundException(exception: ScheduleNotFoundException): ResponseEntity<Any> {
        if (isDebug) {
            exception.printStackTrace()
            return exception.toDebugResponseEntity()
        }
        return exception.toResponseEntity()
    }

    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    @ExceptionHandler(RuntimeException::class)
    fun handleRuntimeException(exception: RuntimeException): ResponseEntity<Any> {
        var response: Any = ErrorResponse(
            message = exception.message ?: "Произошла ошибка во время выполнения запроса!",
            code = exception.javaClass.simpleName,
            status = HttpStatus.INTERNAL_SERVER_ERROR.value())
        if (isDebug) {
            exception.printStackTrace()
            response = (response as ErrorResponse).toDebugResponse(exception)
        }
        return ResponseEntity(response, HttpStatus.INTERNAL_SERVER_ERROR)
    }

    @ExceptionHandler(NoHandlerFoundException::class)
    fun handleNoHandlerFoundException(exception: NoHandlerFoundException): ResponseEntity<Any> {
        var response: Any = ErrorResponse(
            message = "Страница не найдена!",
            code = exception.javaClass.simpleName,
            status = HttpStatus.NOT_FOUND.value()
        )
        if (isDebug) {
            exception.printStackTrace()
            response = (response as ErrorResponse).toDebugResponse(exception)
        }
        return ResponseEntity(response, HttpStatus.NOT_FOUND)
    }

    @ResponseStatus(HttpStatus.NOT_FOUND)
    @ExceptionHandler(UserNotFoundException::class)
    fun handleUserNotFoundException(exception: UserNotFoundException): ResponseEntity<Any> {
        if (isDebug) {
            exception.printStackTrace()
            return exception.toDebugResponseEntity()
        }
        return exception.toResponseEntity()
    }

    @ExceptionHandler(PermissionDeniedException::class)
    fun handlePermissionDeniedException(exception: PermissionDeniedException): ResponseEntity<Any> {
        if (isDebug) {
            exception.printStackTrace()
            return exception.toDebugResponseEntity()
        }
        return exception.toResponseEntity()
    }

    @ExceptionHandler(UnauthorizedException::class)
    fun handleUnauthorizedException(exception: UnauthorizedException): ResponseEntity<Any> {
        if (isDebug) {
            exception.printStackTrace()
            return exception.toDebugResponseEntity()
        }
        return exception.toResponseEntity()
    }

    @ExceptionHandler(SecretKeyParseException::class)
    fun handleSecretKeyParseException(exception: SecretKeyParseException): ResponseEntity<Any> {
        if (isDebug) {
            exception.printStackTrace()
            return exception.toDebugResponseEntity()
        }
        return exception.toResponseEntity()
    }

    @ExceptionHandler(MissingServletRequestParameterException::class)
    fun handleMissingServletRequestParameterException(exception: MissingServletRequestParameterException): ResponseEntity<Any> {
        var response: Any = ErrorResponse(
            message = "Необходимый параметр запроса ${exception.parameterName} типа ${exception.parameterType} не передан!",
            code = exception.javaClass.simpleName,
            status = HttpStatus.BAD_REQUEST.value()
        )
        if (isDebug) {
            exception.printStackTrace()
            response = (response as ErrorResponse).toDebugResponse(exception)
        }
        return ResponseEntity(response, HttpStatus.BAD_REQUEST)
    }

    @ExceptionHandler(HttpMessageNotReadableException::class)
    fun handleHttpMessageNotReadableException(exception: HttpMessageNotReadableException): ResponseEntity<Any> {
        var response: Any = ErrorResponse(
            message = "Необходимое тело запроса не передано!",
            code = exception.javaClass.simpleName,
            status = HttpStatus.BAD_REQUEST.value()
        )
        if (isDebug) {
            exception.printStackTrace()
            response = (response as ErrorResponse).toDebugResponse(exception)
        }
        return ResponseEntity(response, HttpStatus.BAD_REQUEST)
    }

    @ExceptionHandler(IllegalArgumentException::class)
    fun handleIllegalArgumentException(exception: IllegalArgumentException): ResponseEntity<Any> {
        var response: Any = ErrorResponse(
            message = exception.message ?: "Неверный параметр в запросе!",
            code = exception.javaClass.simpleName,
            status = HttpStatus.BAD_REQUEST.value()
        )
        if (isDebug) {
            exception.printStackTrace()
            response = (response as ErrorResponse).toDebugResponse(exception)
        }
        return ResponseEntity(response, HttpStatus.BAD_REQUEST)
    }

    @ExceptionHandler(FileNotFoundException::class)
    fun handleFileNotFoundException(exception: FileNotFoundException): ResponseEntity<Any> {
        var response: Any = ErrorResponse(
            message = exception.message ?: "Файл не найден!",
            code = exception.javaClass.simpleName,
            status = HttpStatus.NOT_FOUND.value()
        )
        if (isDebug) {
            response = (response as ErrorResponse).toDebugResponse(exception)
        }
        return ResponseEntity(response, HttpStatus.NOT_FOUND)
    }
}