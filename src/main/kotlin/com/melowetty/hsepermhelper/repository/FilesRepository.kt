package com.melowetty.hsepermhelper.repository

import org.springframework.core.io.Resource
import java.io.FileNotFoundException
import java.nio.file.Path

interface FilesRepository {
    /**
     * Upload file on server and store in files storage location
     *
     * @param path file path (do not contain file name)
     * @param resource file converted to resource
     * @param fileName name of file
     * @return file path
     */
    fun storeFile(path: Path, resource: Resource, fileName: String): String

    /**
     * Delete file by path
     *
     * @throws FileNotFoundException when file not found on this path
     * @param path file path (contain file name)
     */
    fun deleteFile(path: Path)

    /**
     * Get file as resource on path
     *
     * @throws FileNotFoundException when file not found on this path
     * @param path file path (contain file name)
     * @return file as resource
     */
    fun getFileAsResource(path: Path): Resource

    /**
     * Creates directory on path
     *
     * @param path directory path
     */
    fun createDirectory(path: Path)

    /**
     * Returns true if directory or file is existing
     *
     * @param path directory or file path
     */
    fun isExists(path: Path): Boolean

    /**
     * Returns path, where files are contained
     *
     * @return work path
     */
    fun getFilesPath(): Path
}