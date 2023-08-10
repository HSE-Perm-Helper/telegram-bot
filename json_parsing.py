import json
# -----------  Курсы  ------------- #

with open("./jsons/response_available_courses.json", 'r', encoding="utf-8") as courses:
    courses_data = json.load(courses)

with open("./jsons/response_available_groups.json", 'r', encoding="utf-8") as groups:
    groups_data = json.load(groups)

with open("./jsons/response_available_programs.json", 'r', encoding="utf-8") as programs:
    programs_data = json.load(programs)

with open("./jsons/response_available_subgroups.json", 'r', encoding="utf-8") as subgroups:
    subgroups_data = json.load(subgroups)
