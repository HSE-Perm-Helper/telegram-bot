from api.utils import raise_schedule_exception_when_service_unavailable, \
    raise_user_not_found_exception_when_exception_in_response, get_request, get_request_as_json
from exception.quarter_schedule_not_found_exception import QuarterScheduleNotFoundException
from model.available_for_hiding_lesson import AvailableForHidingLesson
from model.lesson_type import LessonType


async def get_today_lessons(telegram_id: int) -> dict:
    response = await get_request(path=f"/v3/schedule/{telegram_id}/today")
    await raise_schedule_exception_when_service_unavailable(response)

    data = response.json()

    await raise_user_not_found_exception_when_exception_in_response(data)

    return data['response']


async def get_tomorrow_lessons(telegram_id: int) -> dict:
    response = await get_request(path=f"/v3/schedule/{telegram_id}/tomorrow")
    await raise_schedule_exception_when_service_unavailable(response)

    data = response.json()

    await raise_user_not_found_exception_when_exception_in_response(data)

    return data['response']


async def get_available_for_hiding_lessons(telegram_id: int) -> list[AvailableForHidingLesson]:
    response = await get_request(path=f"/schedule/lessons-for-hiding?telegramId={telegram_id}")
    await raise_schedule_exception_when_service_unavailable(response)

    data = response.json()

    if response.status_code != 200:
        await raise_user_not_found_exception_when_exception_in_response(data)
        if data["errorDescription"]["code"] == "ScheduleNotFoundException":
            raise QuarterScheduleNotFoundException()

    return list(map(
        lambda lesson: AvailableForHidingLesson(lesson["lesson"], LessonType[lesson["lessonType"]], lesson["subGroup"]),
        data
    ))


async def get_schedule(telegram_id: int, start: str, end: str) -> dict[str, any]:
    response = await get_request(path=f"/v3/schedule/{telegram_id}?start={start}&end={end}")
    await raise_schedule_exception_when_service_unavailable(response)

    data = response.json()

    await raise_user_not_found_exception_when_exception_in_response(data)

    return data


async def get_schedules() -> dict[str, any]:
    response = await get_request(path=f"/v3/schedules")
    await raise_schedule_exception_when_service_unavailable(response)

    return response.json()


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

async def get_groups(course: int, program: str) -> list[str]:
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
