package com.melowetty.hsepermhelper

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.boot.web.servlet.ServletComponentScan
import org.springframework.web.servlet.config.annotation.EnableWebMvc

@SpringBootApplication
@ServletComponentScan
@EnableWebMvc
class HsePermHelperApplication

fun main(args: Array<String>) {
    runApplication<HsePermHelperApplication>(*args)
}
