package com.melowetty.hsepermhelper.models

import com.fasterxml.jackson.annotation.JsonPropertyOrder
import io.swagger.v3.oas.annotations.media.Schema
import org.apache.commons.lang3.exception.ExceptionUtils

@Schema(description = "Ответ от сервера")
@JsonPropertyOrder("error", "response")
data class Response<T>(
    @Schema(description = "Тело ответа от сервера")
    val response: T,
    @Schema(description = "Наличие ошибки", example = "false")
    val error: Boolean = false,
) {
}

data class ErrorResponse(
    val error: Boolean = true,
    val errorDescription: ErrorDescription
) {
    fun toDebugResponse(exception: Exception): ErrorDebugResponse {
        return ErrorDebugResponse(
            error = true,
            errorDescription = ErrorDebugDescription(
                message = errorDescription.message,
                code = errorDescription.code,
                status = errorDescription.status,
                stacktrace = ExceptionUtils.getStackTrace(exception)
            )
        )
    }
}

data class ErrorDescription(
    val message: String,
    val code: String,
    val status: Int,
)

data class ErrorDebugResponse(
    val error: Boolean = true,
    val errorDescription: ErrorDebugDescription
)

data class ErrorDebugDescription(
    val message: String,
    val code: String,
    val status: Int,
    val stacktrace: String,
)

fun ErrorResponse(
    message: String,
    code: String,
    status: Int,
): ErrorResponse {
    return ErrorResponse(
        error = true,
        errorDescription = ErrorDescription(
            message = message,
            code = code,
            status = status,
        )
    )
}

fun ErrorDebugResponse(
    exception: Exception,
    message: String,
    code: String,
    status: Int,
): ErrorDebugResponse {
    return ErrorDebugResponse(
        error = true,
        errorDescription = ErrorDebugDescription(
            message = message,
            code = code,
            status = status,
            stacktrace = ExceptionUtils.getStackTrace(exception)
        )
    )
}
