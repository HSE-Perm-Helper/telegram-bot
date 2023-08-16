package com.melowetty.hsepermhelper.filters

import com.fasterxml.jackson.databind.ObjectMapper
import com.melowetty.hsepermhelper.exceptions.CustomException
import com.melowetty.hsepermhelper.exceptions.PermissionDeniedException
import com.melowetty.hsepermhelper.exceptions.UnauthorizedException
import com.melowetty.hsepermhelper.models.ErrorResponse
import com.melowetty.hsepermhelper.secrets.SecretKeyManager
import jakarta.servlet.FilterChain
import jakarta.servlet.annotation.WebFilter
import jakarta.servlet.http.HttpServletRequest
import jakarta.servlet.http.HttpServletResponse
import org.springframework.core.env.Environment
import org.springframework.http.HttpStatus
import org.springframework.web.filter.OncePerRequestFilter


@WebFilter
class SecurityFilter(
    private val securityKeyManager: SecretKeyManager,
    private val env: Environment,
): OncePerRequestFilter() {
    override fun doFilterInternal(
        request: HttpServletRequest,
        response: HttpServletResponse,
        filterChain: FilterChain
    ) {
        try {
            val rawLine = env.getProperty("app.secret-key.enable") ?: "true"
            val isSecurityCheckEnabled = rawLine.toBooleanStrictOrNull() ?: true
            if(isSecurityCheckEnabled) {
                val key = request.getHeader("X-Secret-Key")
                    ?: throw UnauthorizedException("Введите секретный ключ в заголовках запроса!")
                val hasAccess: Boolean = securityKeyManager.checkKey(key)
                if (hasAccess) {
                    filterChain.doFilter(request, response)
                    return
                }
                throw PermissionDeniedException("Доступ запрещён!")
            } else {
                filterChain.doFilter(request, response)
            }
        } catch (e: Exception) {
            response.contentType = "application/json"
            if(e is CustomException) {
                val responseEntity = e.toResponseEntity()
                response.status = responseEntity.statusCode.value();
                convertObjectToJson(responseEntity.body)?.let { response.writer.write(it) };
                return
            }
            val responseBody = ErrorResponse(
                message = e.message ?: "",
                code = e.javaClass.simpleName,
                status = HttpStatus.INTERNAL_SERVER_ERROR.value(),
            )
            response.status = HttpStatus.INTERNAL_SERVER_ERROR.value()
            convertObjectToJson(responseBody)?.let { response.writer.write(it) }
        }
    }

    private fun convertObjectToJson(obj: Any?): String? {
        if (obj == null) {
            return null
        }
        val mapper = ObjectMapper()
        return mapper.writeValueAsString(obj)
    }

    override fun shouldNotFilter(request: HttpServletRequest): Boolean {
        val basePath = env.getProperty("server.servlet.context-path")
        if(request.requestURI.startsWith("${basePath}/files")) return true
        if(request.requestURI.startsWith("${basePath}${env.getProperty("springdoc.swagger-ui.path")}")) return true
        if(request.requestURI.startsWith("${basePath}/swagger-ui")) return true
        if(request.requestURI.startsWith("${basePath}/v3/api-docs")) return true
        return super.shouldNotFilter(request)
    }
}