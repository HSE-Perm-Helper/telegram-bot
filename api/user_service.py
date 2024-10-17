from api.utils import raise_user_not_found_exception_when_exception_in_response, get_request_as_json, \
    patch_request_as_json, get_request, post_request_as_json, post_request, delete_request
from model.available_for_hiding_lesson import AvailableForHidingLesson
from model.hidden_lesson import HiddenLesson
from model.lesson_type import LessonType


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


async def get_admin_ids() -> list[int]:
    return [646596194, 774471737]


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

    await raise_user_not_found_exception_when_exception_in_response(user)

    return user["response"]["settings"]


async def get_user_hidden_lessons(telegram_id: int) -> list[HiddenLesson]:
    user = await get_request_as_json(path=f"/user?telegramId={telegram_id}")

    await raise_user_not_found_exception_when_exception_in_response(user)

    data = user["response"]["settings"]["hiddenLessons"]

    return list(map(
        lambda lesson: HiddenLesson(lesson["lesson"], LessonType[lesson["lessonType"]], lesson["subGroup"]), data
    ))


async def add_user_hidden_lesson(telegram_id: int, lesson: AvailableForHidingLesson) -> None:
    data = {
        "lesson": lesson.lesson,
        "lessonType": lesson.lesson_type.name,
        "subGroup": lesson.sub_group,
    }

    await post_request(path=f"/user/hidden-lessons?telegramId={telegram_id}", json=data)


async def remove_user_hidden_lesson(telegram_id: int, lesson: AvailableForHidingLesson) -> None:
    data = {
        "lesson": lesson.lesson,
        "lessonType": lesson.lesson_type.name,
        "subGroup": lesson.sub_group,
    }

    await delete_request(path=f"/user/hidden-lessons?telegramId={telegram_id}", json=data)


async def check_registration_user(telegram_id: int) -> bool:
    response = await get_request(path=f"/user?telegramId={telegram_id}")
    return response.status_code == 200