from api.utils import get_request, raise_schedule_exception_when_service_unavailable, \
    raise_user_not_found_exception_when_exception_in_response, get_request_as_json, post_request, delete_request
from exception.quarter_schedule_not_found_exception import QuarterScheduleNotFoundException
from model.available_for_hiding_lesson import AvailableForHidingLesson
from model.hidden_lesson import HiddenLesson
from model.lesson_type import LessonType


async def get_available_for_hiding_lessons(telegram_id: int) -> list[AvailableForHidingLesson]:
    response = await get_request(path=f"/v3/users/{telegram_id}/settings/hidden-lessons")
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


async def get_user_hidden_lessons(telegram_id: int) -> list[HiddenLesson]:
    user = await get_request_as_json(path=f"/v3/users/{telegram_id}")

    await raise_user_not_found_exception_when_exception_in_response(user)

    data = user["settings"]["hiddenLessons"]

    return list(map(
        lambda lesson: HiddenLesson(lesson["lesson"], LessonType[lesson["lessonType"]], lesson["subGroup"]), data
    ))


async def add_user_hidden_lesson(telegram_id: int, lesson: AvailableForHidingLesson) -> None:
    data = {
        "lesson": lesson.lesson,
        "lessonType": lesson.lesson_type.name,
        "subGroup": lesson.sub_group,
    }

    await post_request(path=f"/v3/users/{telegram_id}/settings/hidden-lessons", json=data)


async def remove_user_hidden_lesson(telegram_id: int, lesson: AvailableForHidingLesson) -> None:
    data = {
        "lesson": lesson.lesson,
        "lessonType": lesson.lesson_type.name,
        "subGroup": lesson.sub_group,
    }

    await delete_request(path=f"/v3/users/{telegram_id}/settings/hidden-lessons", json=data)