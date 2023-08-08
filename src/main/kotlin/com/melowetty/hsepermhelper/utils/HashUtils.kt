package com.melowetty.hsepermhelper.utils

import java.io.File
import java.security.MessageDigest

fun getHash(file: File): String {
    val digest = MessageDigest.getInstance("SHA-256")
    val hexArray = "0123456789ABCDEF"
    val bytes = digest.digest(file.readBytes())
    val hash = StringBuilder(bytes.size * 2)
    bytes.forEach {
        val i = it.toInt()
        hash.append(hexArray[i shr 4 and 0x0f])
        hash.append(hexArray[i and 0x0f])
    }
    return hash.toString()
}

fun checkHash(file: File, expectedHash: String): Boolean {
    val hash = getHash(file)
    return expectedHash == hash
}