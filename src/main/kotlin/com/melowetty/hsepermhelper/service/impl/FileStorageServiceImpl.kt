package com.melowetty.hsepermhelper.service.impl

import com.melowetty.hsepermhelper.models.Response
import com.melowetty.hsepermhelper.repository.FilesRepository
import com.melowetty.hsepermhelper.service.FileStorageService
import com.melowetty.hsepermhelper.service.UserService
import com.melowetty.hsepermhelper.utils.FileUtils
import org.springframework.core.io.Resource
import org.springframework.http.ResponseEntity
import org.springframework.stereotype.Component
import java.nio.file.Path
import kotlin.io.path.name

@Component
class FileStorageServiceImpl(
    private val fileStorageRepository: FilesRepository,
    private val userService: UserService
): FileStorageService {
    override fun storeFile(path: Path, resource: Resource, fileName: String): Response<String> {
        val response = fileStorageRepository.storeFile(path = path, resource = resource, fileName = fileName)
        return Response(response)
    }

    override fun getFile(path: Path): ResponseEntity<Resource> {
        return FileUtils.getFileDownloadResponse(fileStorageRepository.getFileAsResource(path), path.fileName.name)
    }
}