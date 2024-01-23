from utils import get_request, get_request_as_json, \
    patch_request_as_json, post_request_as_json


# ------------ Пользователи --------- #

def get_user_ids() -> list[int]:
    user_ids: list[int] = []
    users = get_request_as_json("/users")
    for user in users["response"]:
        user_ids.append(int(user['telegramId']))
    return user_ids


# -------------  Курсы  ------------- #

def get_courses() -> list[int]:
    courses: list[int] = []
    courses_data = get_request_as_json("/schedule/available_courses")
    for i in courses_data["response"]:
        courses.append(int(i))

    return courses


# -------------  Программы  ------------- #

def get_programs(course: int) -> list[str]:
    programs: list[str] = []
    programs_data = get_request_as_json(f"/schedule/available_programs?course={course}")
    for i in programs_data["response"]:
        programs.append(i)

    return programs


# -------------  Группы  ------------- #

def get_groups(course: int, program: int) -> list[str]:
    groups: list[str] = []
    groups_data = get_request_as_json(path=f"/schedule/available_groups?course={course}"
                                           f"&program={program}")
    for i in groups_data["response"]:
        groups.append(i)

    return groups


# -------------  Подгруппы  ------------- #

def get_subgroups(course: int, program: str, group: str) -> list[int]:
    subgroups: list[int] = []
    subgroups_data = get_request_as_json(path=f"/schedule/available_subgroups?course={course}"
                                              f"&program={program}&group={group}")
    for i in subgroups_data["response"]:
        subgroups.append(int(i))

    return subgroups


# -------------  Регистрация пользователя  ------------- #


def registration_user(telegram_id: int, group: str, subgroup: int) -> bool:
    user_data = post_request_as_json(path=f"/users",
                                     json={
                                         "telegramId": int(telegram_id),
                                         "settings": {
                                             "group": group,
                                             "subGroup": subgroup
                                         }
                                     })
    return bool(user_data['error'])


def edit_user(telegram_id: int, group: str, subgroup: int) -> bool:
    copied_subgroup = subgroup
    if subgroup == 0:
        copied_subgroup = None
    user_data = patch_request_as_json(path=f"/user?telegramId={telegram_id}",
                                      json={
                                          "group": group,
                                          "subGroup": copied_subgroup
                                      })
    return bool(user_data['error'])


# -------------  Получение расписания  ------------- #

def get_schedule(telegram_id: int) -> dict[str, any]:
    schedule_data = get_request_as_json(path=f"/v2/schedule/{telegram_id}")
    return schedule_data


# -------------  Проверка обновления расписания  ------------- #


def check_registration_user(telegram_id: int) -> bool:
    response = get_request(path=f"/user?telegramId={telegram_id}")
    return response.status_code == 200
