package com.melowetty.hsepermhelper.repository

import org.springframework.core.io.Resource
import java.nio.file.Path

interface FilesRepository {
    fun storeFile(path: Path, resource: Resource, fileName: String): String
    fun getFileAsResource(path: Path): Resource
}