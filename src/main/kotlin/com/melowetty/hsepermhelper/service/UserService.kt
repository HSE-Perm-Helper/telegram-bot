package com.melowetty.hsepermhelper.service

import com.melowetty.hsepermhelper.dto.UserDto

interface UserService {

    /**
     * Method returns user by he/she telegram ID
     * @param telegramId telegram ID of user
     * @return returns user object when it is found or null else
     */
    fun getByTelegramId(telegramId: Long): UserDto

    /**
     * Method creates user and return telegram ID when operation have success
     * @param dto User object
     * @return telegram ID
     */
    fun create(dto: UserDto): Long
}