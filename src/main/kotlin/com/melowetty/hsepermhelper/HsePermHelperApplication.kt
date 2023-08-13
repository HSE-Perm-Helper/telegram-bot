package com.melowetty.hsepermhelper

import com.melowetty.hsepermhelper.config.FileStorageConfig
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.context.properties.EnableConfigurationProperties
import org.springframework.boot.runApplication
import org.springframework.boot.web.servlet.ServletComponentScan
import org.springframework.web.servlet.config.annotation.EnableWebMvc

@EnableConfigurationProperties(
    FileStorageConfig::class
)
@SpringBootApplication
@ServletComponentScan
@EnableWebMvc
class HsePermHelperApplication

fun main(args: Array<String>) {
    runApplication<HsePermHelperApplication>(*args)
}
