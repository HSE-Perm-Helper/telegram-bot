import json
import requests

base_url = "https://hse-schedule-bot.xenforo-studio.ru/api"
x_secret_key = "56mx-0=l08u58%i&tp-@xz*2&d0tyhjn#^l3qk&ch@z)9foc"
accept_data = "application/json"
headers = {"X-Secret-Key": x_secret_key, "Accept": accept_data, "Content-Type": "application/json; charset=utf-8"}

# ---------------------------------  Данные пользователя  ----------------------------------- #

user_data_list = [0] * 4  # Данные для идентификации пользователя, 1 - курс, 2 - направление, 3 - группа, 4 - подгруппа


# -----------  Курсы  ------------- #

def get_courses():
    courses = []
    courses_json = requests.get(
        url=f"{base_url}/schedule/available_courses",
        headers=headers,
    )
    courses_data = courses_json.json()
    for i in courses_data["response"]:
        courses.append(i)

    return courses


# -----------  Программы  ------------- #

def get_programs():
    programs = []
    programs_json = requests.get(
        url=f"{base_url}/schedule/available_programs?course={user_data_list[0]}",
        headers=headers)
    programs_data = programs_json.json()
    for i in programs_data["response"]:
        programs.append(i)

    return programs


# -----------  Группы  ------------- #

def get_groups():
    groups = []
    groups_json = requests.get(
        url=f"{base_url}/schedule/available_groups?course={user_data_list[0]}"
            f"&program={user_data_list[1]}",
        headers=headers)
    groups_data = groups_json.json()
    print(groups_data)
    for i in groups_data["response"]:
        groups.append(i)

    return groups


# -----------  Подгруппы  ------------- #

def get_subgroups():
    subgroups = []
    subgroups_json = requests.get(
        url=f"{base_url}/schedule/available_subgroups?course={user_data_list[0]}"
            f"&program={user_data_list[1]}&group={user_data_list[2]}",
        headers=headers)
    subgroups_data = subgroups_json.json()
    for i in subgroups_data["response"]:
        subgroups.append(i)

    return subgroups