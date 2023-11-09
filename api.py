import requests

import venv

base_url = venv.base_url
x_secret_key = venv.x_secret_key
accept_data = "application/json"
headers = {"X-Secret-Key": x_secret_key, "Accept": accept_data, "Content-Type": "application/json; charset=utf-8"}


# -------------  Курсы  ------------- #

def get_courses():
    courses = []
    courses_json = requests.get(
        url=f"{base_url}/schedule/available_courses",
        headers=headers,
        verify=False
    )
    courses_data = courses_json.json()
    for i in courses_data["response"]:
        courses.append(i)

    return courses


# -------------  Программы  ------------- #

def get_programs(number_course):
    programs = []
    programs_json = requests.get(
        url=f"{base_url}/schedule/available_programs?course={number_course}",
        headers=headers,
        verify=False)
    programs_data = programs_json.json()
    for i in programs_data["response"]:
        programs.append(i)

    return programs


# -------------  Группы  ------------- #

def get_groups(number_course, number_program):
    groups = []
    groups_json = requests.get(
        url=f"{base_url}/schedule/available_groups?course={number_course}"
            f"&program={number_program}",
        headers=headers,
        verify=False)
    groups_data = groups_json.json()
    for i in groups_data["response"]:
        groups.append(i)

    return groups


# -------------  Подгруппы  ------------- #

def get_subgroups(number_course, number_program, number_group):
    subgroups = []
    subgroups_json = requests.get(
        url=f"{base_url}/schedule/available_subgroups?course={number_course}"
            f"&program={number_program}&group={number_group}",
        headers=headers,
        verify=False)
    subgroups_data = subgroups_json.json()
    for i in subgroups_data["response"]:
        subgroups.append(i)

    return subgroups


# -------------  Регистрация пользователя  ------------- #


def registration_user(data):
    course, program, group, subgroup, telegram_id, is_new_user = data.split("^")
    if subgroup != "None":
        subgroup = int(subgroup)
    else:
        subgroup = 0
    answer = requests.post(url=f"{base_url}/users",
                           json={
                               "telegramId": int(telegram_id),
                               "settings": {
                                   "group": group,
                                   "subGroup": subgroup
                               }
                           }, headers=headers,
                           verify=False)
    answer = answer.json()
    return answer['error']


def edit_user(data):
    course, program, group, subgroup, telegram_id, is_new_user = data.split("^")
    if subgroup != "None":
        subgroup = int(subgroup)
    else:
        subgroup = None
    response = requests.patch(url=f"{base_url}/user?telegramId={telegram_id}",
                              json={
                                  "group": group,
                                  "subGroup": subgroup
                              }, headers=headers,
                              verify=False)
    response = response.json()
    print(response['error'])
    return response['error']


# -------------  Получение расписания  ------------- #

def get_schedule(telegram_id):
    response = requests.get(url=f"{base_url}/schedule/{telegram_id}",
                            headers=headers,
                            verify=False)
    response = response.json()
    return response


# -------------  Проверка обновления расписания  ------------- #


def check_registration_user(telegram_id):
    response = requests.get(
        url=f"{base_url}/user?telegramId={telegram_id}",
        headers=headers,
        verify=False)
    return response.status_code == 200


