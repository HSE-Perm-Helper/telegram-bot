from api.utils import get_request_as_json


async def get_courses() -> list[int]:
    courses: list[int] = []
    courses_data = await get_request_as_json("/v1/schedule-info/courses")
    for i in courses_data["response"]:
        courses.append(int(i))

    return courses


# -------------  Программы  ------------- #

async def get_programs(course: int) -> list[str]:
    programs: list[str] = []
    programs_data = await get_request_as_json(f"/v1/schedule-info/programs?course={course}")
    for i in programs_data["response"]:
        programs.append(i)

    return programs


# -------------  Группы  ------------- #

async def get_groups(course: int, program: str) -> list[str]:
    groups: list[str] = []
    groups_data = await get_request_as_json(path=f"/v1/schedule-info/groups?course={course}"
                                                 f"&program={program}")
    for i in groups_data["response"]:
        groups.append(i)

    return groups
