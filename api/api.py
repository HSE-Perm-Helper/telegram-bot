from util.utils import get_request, get_request_as_json, \
    patch_request_as_json, post_request_as_json


# ------------ Пользователи --------- #

async def get_user_ids() -> list[int]:
    user_ids: list[int] = []
    users = await get_request_as_json("/users")
    for user in users["response"]:
        user_ids.append(int(user['telegramId']))
    return user_ids


async def get_user_ids_by_course(course: int) -> list[int]:
    user_ids: list[int] = []
    users = await get_request_as_json("/users")
    for user in users["response"]:
        group = user["settings"]["group"]
        num = int(group.split("-")[1])
        user_course = 25 - num
        if user_course == course:
            user_ids.append(int(user['telegramId']))
    return user_ids


# ---------- Администраторы -----------#

async def get_admin_ids() -> list[int]:
    return [646596194, 774471737]


# -------------  Курсы  ------------- #

async def get_courses() -> list[int]:
    courses: list[int] = []
    courses_data = await get_request_as_json("/schedule/available_courses")
    for i in courses_data["response"]:
        courses.append(int(i))

    return courses


# -------------  Программы  ------------- #

async def get_programs(course: int) -> list[str]:
    programs: list[str] = []
    programs_data = await get_request_as_json(f"/schedule/available_programs?course={course}")
    for i in programs_data["response"]:
        programs.append(i)

    return programs


# -------------  Группы  ------------- #

async def get_groups(course: int, program: int) -> list[str]:
    groups: list[str] = []
    groups_data = await get_request_as_json(path=f"/schedule/available_groups?course={course}"
                                                 f"&program={program}")
    for i in groups_data["response"]:
        groups.append(i)

    return groups


# -------------  Подгруппы  ------------- #

async def get_subgroups(course: int, program: str, group: str) -> list[int]:
    subgroups: list[int] = []
    subgroups_data = await get_request_as_json(path=f"/schedule/available_subgroups?course={course}"
                                                    f"&program={program}&group={group}")
    for i in subgroups_data["response"]:
        subgroups.append(int(i))

    return subgroups


# -------------  Регистрация пользователя  ------------- #


async def registration_user(telegram_id: int, group: str, subgroup: int) -> bool:
    user_data = await post_request_as_json(path=f"/users",
                                           json={
                                               "telegramId": int(telegram_id),
                                               "settings": {
                                                   "group": group,
                                                   "subGroup": subgroup
                                               }
                                           })
    return not bool(user_data['error'])


async def edit_user(telegram_id: int, group: str, subgroup: int) -> bool:
    user_data = await patch_request_as_json(path=f"/user?telegramId={telegram_id}",
                                            json={
                                                "group": group,
                                                "subGroup": subgroup
                                            })
    return not bool(user_data['error'])


async def edit_user_settings(telegram_id: int, setting: str, new_value: bool) -> bool:
    user_data = await patch_request_as_json(path=f"/user?telegramId={telegram_id}",
                                            json={
                                                f"{setting}": new_value,
                                            })
    return not bool(user_data['error'])


async def get_user_settings(telegram_id: int) -> dict | None:
    user = await get_request_as_json(path=f"/user?telegramId={telegram_id}")
    if user["error"]:
        return None
    return user["response"]["settings"]


# -------------  Получение расписания  ------------- #

async def get_schedule(telegram_id: int, start: str, end: str) -> dict[str, any]:
    schedule_data = await get_request_as_json(path=f"/v3/schedule/{telegram_id}?start={start}&end={end}")
    return schedule_data


async def get_schedules() -> dict[str, any]:
    schedule_data = await get_request_as_json(path=f"/v3/schedules")
    return schedule_data


# -------------  Проверка обновления расписания  ------------- #


async def check_registration_user(telegram_id: int) -> bool:
    response = await get_request(path=f"/user?telegramId={telegram_id}")
    return response.status_code == 200


# ----------- Автообновляемое расписание -------------- #

async def get_remote_schedule_link(telegram_id: int) -> str:
    response = await get_request_as_json(path=f"/schedule/{telegram_id}/download")
    print(response)
    return f'{response["response"]["linkForRemoteCalendar"]}'


async def get_today_lessons(telegram_id: int) -> dict:
    response = await get_request_as_json(path=f"/v3/schedule/{telegram_id}/today")
    return response['response']


async def get_tomorrow_lessons(telegram_id: int) -> dict:
    response = await get_request_as_json(path=f"/v3/schedule/{telegram_id}/tomorrow")
    return response['response']
