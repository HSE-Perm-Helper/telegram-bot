package com.melowetty.hsepermhelper.config

import io.swagger.v3.oas.annotations.OpenAPIDefinition
import io.swagger.v3.oas.annotations.enums.SecuritySchemeIn
import io.swagger.v3.oas.annotations.enums.SecuritySchemeType
import io.swagger.v3.oas.annotations.info.Contact
import io.swagger.v3.oas.annotations.info.Info
import io.swagger.v3.oas.annotations.security.SecurityScheme

@OpenAPIDefinition(
    info = Info(
        title = "HSE Perm Schedule API",
        description = "Melowetty", version = "1.0.1",
        contact = Contact(
            name = "Denis Malinin",
            email = "melowetty@mail.ru",
            url = "https://github.com/Melowetty"
        )
    )
)
@SecurityScheme(
    name = "X-Secret-Key",
    type = SecuritySchemeType.APIKEY,
    description = "Секретный ключ",
    `in` = SecuritySchemeIn.HEADER,
    paramName = "X-Secret-Key"
)
class OpenApiConfig {
}