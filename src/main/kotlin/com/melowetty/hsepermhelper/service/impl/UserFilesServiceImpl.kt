package com.melowetty.hsepermhelper.service.impl

import com.melowetty.hsepermhelper.dto.UserDto
import com.melowetty.hsepermhelper.events.EventType
import com.melowetty.hsepermhelper.events.UsersChangedEvent
import com.melowetty.hsepermhelper.service.FileStorageService
import com.melowetty.hsepermhelper.service.UserFilesService
import org.springframework.context.event.EventListener
import org.springframework.core.io.Resource
import org.springframework.stereotype.Service
import java.nio.file.Path
import kotlin.io.path.Path

@Service
class UserFilesServiceImpl(
    private val fileStorageService: FileStorageService
): UserFilesService {
    private final val basePath = Path("user_files")
    init {
        try {
            if (fileStorageService.isExists(basePath).not()) {
                fileStorageService.createDirectory(basePath)
            }
        } catch (e: Exception) {
            throw RuntimeException("Не удалось создать директорию для хранения файлов пользователей.", e)
        }
    }

    @EventListener
    fun handleUsersChanging(event: UsersChangedEvent) {
        if(event.type == EventType.DELETED) {
            deleteUserFolder(event.source)
        }
    }

    override fun storeFile(user: UserDto, path: Path, resource: Resource, fileName: String): String {
        val userPath = basePath.resolve(user.id.toString()).resolve(path)
        fileStorageService.storeFile(userPath, resource, fileName)
        return fileName
    }

    override fun storeFile(user: UserDto, resource: Resource, fileName: String): String {
        return storeFile(user, Path(""), resource, fileName)
    }

    override fun deleteFile(user: UserDto, path: Path) {
        val userPath = basePath.resolve(user.id.toString()).resolve(path)
        fileStorageService.deleteFile(userPath)
    }

    override fun getFilesPath(): Path {
        return fileStorageService.getFilesPath().resolve(basePath)
    }

    override fun getUserFilesPath(user: UserDto): Path {
        return getFilesPath().resolve(user.id.toString())
    }

    override fun getFile(path: Path): Resource {
        return fileStorageService.getFile(basePath.resolve(path))
    }

    private fun deleteUserFolder(user: UserDto) {
        fileStorageService.deleteFile(basePath.resolve(user.id.toString()))
    }
}