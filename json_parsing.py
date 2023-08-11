import json

# -----------  Курсы  ------------- #
courses = []

with open("./jsons/response_available_courses.json", 'r', encoding="utf-8") as courses_json:
    courses_data = json.load(courses_json)
    for i in courses_data["response"]:
        courses.append(i)

# -----------  Группы  ------------- #
groups = []

with open("./jsons/response_available_groups.json", 'r', encoding="utf-8") as groups_json:
    groups_data = json.load(groups_json)
    for i in groups_data["response"]:
        groups.append(i)

# -----------  Программы  ------------- #
programs = []

with open("./jsons/response_available_programs.json", 'r', encoding="utf-8") as programs_json:
    programs_data = json.load(programs_json)
    for i in programs_data["response"]:
        programs.append(i)

# -----------  Подгруппы  ------------- #
subgroups = []

with open("./jsons/response_available_subgroups.json", 'r', encoding="utf-8") as subgroups_json:
    subgroups_data = json.load(subgroups_json)
    for i in subgroups_data["response"]:
        subgroups.append(i)
