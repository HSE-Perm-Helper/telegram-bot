package com.melowetty.hsepermhelper.utils

import jakarta.servlet.http.HttpServletRequest
import org.springframework.web.servlet.support.ServletUriComponentsBuilder


class UrlUtils {
    companion object {
        /**
         * This method to get base URL of the application
         * @param request the HttpServletRequest object
         * @return the base URL
         */
        fun getBaseUrl(request: HttpServletRequest): String {
            return ServletUriComponentsBuilder
                .fromRequestUri(request)
                .replacePath(null)
                .build()
                .toUriString()
        }
    }
}