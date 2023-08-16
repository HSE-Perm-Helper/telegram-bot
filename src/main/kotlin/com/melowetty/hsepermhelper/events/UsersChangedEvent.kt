package com.melowetty.hsepermhelper.events

import com.melowetty.hsepermhelper.dto.UserDto

class UsersChangedEvent(
    user: UserDto,
    type: EventType
): CustomEvent<UserDto>(user, type)