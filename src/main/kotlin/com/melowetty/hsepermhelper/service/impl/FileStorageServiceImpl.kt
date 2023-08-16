package com.melowetty.hsepermhelper.service.impl

import com.melowetty.hsepermhelper.repository.FilesRepository
import com.melowetty.hsepermhelper.service.FileStorageService
import org.springframework.core.io.Resource
import org.springframework.stereotype.Component
import java.nio.file.Path

@Component
class FileStorageServiceImpl(
    private val fileStorageRepository: FilesRepository,
): FileStorageService {
    override fun storeFile(path: Path, resource: Resource, fileName: String): String {
        return fileStorageRepository.storeFile(path = path, resource = resource, fileName = fileName)
    }

    override fun deleteFile(path: Path) {
        fileStorageRepository.deleteFile(path)
    }

    override fun getFile(path: Path): Resource {
        return fileStorageRepository.getFileAsResource(path)
    }

    override fun createDirectory(path: Path) {
        fileStorageRepository.createDirectory(path)
    }

    override fun isExists(path: Path): Boolean {
        return fileStorageRepository.isExists(path)
    }

    override fun getFilesPath(): Path {
        return getFilesPath()
    }
}