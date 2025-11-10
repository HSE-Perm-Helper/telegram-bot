from typing_extensions import deprecated

from api.utils import raise_schedule_exception_when_service_unavailable, \
    raise_user_not_found_exception_when_exception_in_response, get_request, get_request_as_json


@deprecated("use timetable_service")
async def get_schedule(telegram_id: int, start: str, end: str) -> dict[str, any]:
    response = await get_request(path=f"/v3/schedule/{telegram_id}?start={start}&end={end}")
    await raise_schedule_exception_when_service_unavailable(response)

    data = response.json()

    await raise_user_not_found_exception_when_exception_in_response(data)

    return data


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
