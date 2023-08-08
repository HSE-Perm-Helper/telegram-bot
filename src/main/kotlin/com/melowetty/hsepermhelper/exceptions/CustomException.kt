package com.melowetty.hsepermhelper.exceptions

import com.melowetty.hsepermhelper.models.ErrorResponse
import org.springframework.http.HttpStatusCode
import org.springframework.http.ResponseEntity

abstract class CustomException(
    override val message: String,
    private val statusCode: HttpStatusCode
    ): Exception(message) {
        fun toResponseEntity(): ResponseEntity<ErrorResponse> {
            val response = ErrorResponse(
                message = message,
                code = javaClass.simpleName,
                status = statusCode.value()
            )
            return ResponseEntity<ErrorResponse>(response, statusCode)
        }
}