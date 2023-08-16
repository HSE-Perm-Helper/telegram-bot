package com.melowetty.hsepermhelper.service

import com.melowetty.hsepermhelper.dto.UserDto
import org.springframework.core.io.Resource
import java.io.FileNotFoundException
import java.nio.file.Path

interface UserFilesService {
    /**
     * Upload file on server and store in files storage location
     *
     * @param user user
     * @param path file path (do not contain file name)
     * @param resource file converted to resource
     * @param fileName name of file
     * @return file name
     */
    fun storeFile(user: UserDto, path: Path, resource: Resource, fileName: String): String

    /**
     * Upload file on server and store in files storage location
     *
     * @param user user
     * @param resource file converted to resource
     * @param fileName name of file
     * @return file name
     */
    fun storeFile(user: UserDto, resource: Resource, fileName: String): String

    /**
     * Delete file by path
     *
     * @throws FileNotFoundException when file not found on this path
     * @param user user
     * @param path file path (contain file name)
     */
    fun deleteFile(user: UserDto, path: Path)

    /**
     * Returns files path
     *
     * @return files path
     */
    fun getFilesPath(): Path

    /**
     * Returns user files path
     *
     * @param user user
     * @return user files path
     */
    fun getUserFilesPath(user: UserDto): Path

    /**
     * Gets user file via path
     *
     * @param path path in user files directory
     * @return file as resource
     */
    fun getFile(path: Path): Resource
}