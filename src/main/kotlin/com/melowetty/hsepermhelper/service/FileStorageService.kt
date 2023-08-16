package com.melowetty.hsepermhelper.service

import org.springframework.core.io.Resource
import java.nio.file.Path

interface FileStorageService {
    fun storeFile(path: Path, resource: Resource, fileName: String): String
    fun deleteFile(path: Path)
    fun getFile(path: Path): Resource
    fun createDirectory(path: Path)
    fun isExists(path: Path): Boolean
    fun getFilesPath(): Path
}