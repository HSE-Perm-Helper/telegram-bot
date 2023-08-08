package com.melowetty.hsepermhelper.secrets

import com.melowetty.hsepermhelper.exceptions.SecretKeyParseException
import org.springframework.core.env.Environment
import org.springframework.stereotype.Component
import java.io.BufferedReader
import java.io.FileReader


@Component
class SecretKeyManager(
    env: Environment
) {
    private val path = env.getProperty("app.secret-key.path") ?: "secret_key.txt"
    private val SECRET_KEY = getSecretKey()
    fun checkKey(key: String?): Boolean {
        if (key == null) return false
        return SECRET_KEY == key
    }

    private fun getSecretKey(): String {
        try {
            BufferedReader(FileReader(path)).use { br ->
                val sb = StringBuilder()
                var line = br.readLine()
                while (line != null) {
                    sb.append(line)
                    sb.append(System.lineSeparator())
                    line = br.readLine()
                }
                return sb.toString().trim()
            }
        } catch (e: Exception) {
            throw SecretKeyParseException("Ошибка проверки секретного ключа. Сервер недоступен.")
        }
    }
}