package com.melowetty.hsepermhelper.controllers

import com.melowetty.hsepermhelper.service.FileStorageService
import com.melowetty.hsepermhelper.utils.FileUtils
import jakarta.servlet.http.HttpServletRequest
import org.springframework.core.io.Resource
import org.springframework.http.ResponseEntity
import org.springframework.stereotype.Controller
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import kotlin.io.path.Path


@Controller
@RequestMapping("files")
class FileStorageController(
    private val fileStorageService: FileStorageService,
) {
    @GetMapping("/**")
    fun getFile(request: HttpServletRequest): ResponseEntity<Resource> {
        val path = FileUtils.extractFilePath(request)
        val filePath = Path(path)
        return fileStorageService.getFile(filePath)
    }
}