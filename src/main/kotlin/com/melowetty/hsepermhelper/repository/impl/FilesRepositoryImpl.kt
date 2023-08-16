package com.melowetty.hsepermhelper.repository.impl

import com.melowetty.hsepermhelper.config.FileStorageConfig
import com.melowetty.hsepermhelper.repository.FilesRepository
import org.springframework.core.io.Resource
import org.springframework.core.io.UrlResource
import org.springframework.stereotype.Component
import org.springframework.util.FileSystemUtils
import java.io.FileNotFoundException
import java.io.IOException
import java.net.MalformedURLException
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import java.nio.file.StandardCopyOption


@Component
class FilesRepositoryImpl(
    private val fileStorageConfig: FileStorageConfig,
): FilesRepository {
    private final val fileStorageLocation: Path = Paths.get(fileStorageConfig.path)
        .toAbsolutePath().normalize()

    init {
        try {
            if (Files.exists(fileStorageLocation).not()) {
                Files.createDirectories(fileStorageLocation)
            }
        } catch (e: Exception) {
            throw RuntimeException("Не удалось создать директорию для хранения файлов.", e)
        }
    }

    override fun storeFile(path: Path, resource: Resource, fileName: String): String {
        return try {
            if (fileName.contains("..")) {
                throw RuntimeException("Имя файла содержит неправильное расширение: $fileName")
            }

            val targetLocation = fileStorageLocation.resolve(path).resolve(fileName)

            val directoryPath = fileStorageLocation.resolve(path)
            if(Files.exists(directoryPath).not()) {
                Files.createDirectory(fileStorageLocation.resolve(path))
            }
            Files.copy(resource.inputStream, targetLocation, StandardCopyOption.REPLACE_EXISTING)
            fileName
        } catch (e: IOException) {
            e.printStackTrace()
            throw RuntimeException("Не удалось сохранить $fileName. Попробуйте ещё раз!", e)
        }
    }

    override fun deleteFile(path: Path) {
        val isSuccess = FileSystemUtils.deleteRecursively(fileStorageLocation.resolve(path))
        if (isSuccess.not()) throw FileNotFoundException("Файл по по пути $path не найден!")
    }

    override fun getFileAsResource(path: Path): Resource {
        return try {
            val filePath: Path = fileStorageLocation.resolve(path).normalize()
            val resource: Resource = UrlResource(filePath.toUri())
            if (resource.exists()) {
                resource
            } else {
                throw FileNotFoundException("Файл по пути $path не найден!")
            }
        } catch (ex: MalformedURLException) {
            throw FileNotFoundException("Файл по пути $path не найден!")
        }
    }

    override fun createDirectory(path: Path) {
        Files.createDirectory(fileStorageLocation.resolve(path))
    }

    override fun isExists(path: Path): Boolean {
        return Files.exists(fileStorageLocation.resolve(path))
    }

    override fun getFilesPath(): Path {
        return fileStorageLocation
    }
}