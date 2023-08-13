package com.melowetty.hsepermhelper.config

import org.springframework.boot.context.properties.ConfigurationProperties

@ConfigurationProperties(prefix = "file-storage")
class FileStorageConfig(
    val path: String,
)