package com.melowetty.hsepermhelper.service

import com.melowetty.hsepermhelper.models.Response
import org.springframework.core.io.Resource
import org.springframework.http.ResponseEntity
import java.nio.file.Path

interface FileStorageService {
    fun storeFile(path: Path, resource: Resource, fileName: String): Response<String>
    fun getFile(path: Path): ResponseEntity<Resource>
}