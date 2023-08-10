package com.melowetty.hsepermhelper.models

import com.fasterxml.jackson.annotation.JsonPropertyOrder
import io.swagger.v3.oas.annotations.media.Schema

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
)

data class ErrorDescription(
    val message: String,
    val code: String,
    val status: Int,
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
