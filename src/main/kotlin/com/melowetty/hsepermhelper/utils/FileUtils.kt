package com.melowetty.hsepermhelper.utils

import jakarta.servlet.http.HttpServletRequest
import org.springframework.core.io.Resource
import org.springframework.http.HttpHeaders
import org.springframework.http.MediaType
import org.springframework.http.ResponseEntity
import org.springframework.util.AntPathMatcher
import org.springframework.web.servlet.HandlerMapping


class FileUtils {
    companion object {
        /**
         * Gets file download response entity from resource
         *
         * @param resource file
         * @param fileName must contains file extension
         * @return response entity with file
         */
        fun getFileDownloadResponse(resource: Resource, fileName: String): ResponseEntity<Resource> {
            val header = HttpHeaders()
            header.add(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=${fileName}")
            header.add("Cache-Control", "no-cache, no-store, must-revalidate")
            header.add("Pragma", "no-cache")
            header.add("Expires", "0")

            return ResponseEntity
                .ok()
                .headers(header)
                .contentType(MediaType.APPLICATION_OCTET_STREAM)
                .body(resource)
        }

        fun extractFilePath(request: HttpServletRequest): String {
            val path = request.getAttribute(
                HandlerMapping.PATH_WITHIN_HANDLER_MAPPING_ATTRIBUTE
            ) as String
            val bestMatchPattern = request.getAttribute(
                HandlerMapping.BEST_MATCHING_PATTERN_ATTRIBUTE
            ) as String
            val apm = AntPathMatcher()
            return apm.extractPathWithinPattern(bestMatchPattern, path)
        }
    }
}