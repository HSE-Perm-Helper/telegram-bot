from api.utils import get_request, raise_schedule_exception_when_service_unavailable, \
    raise_user_not_found_exception_when_exception_in_response, has_error_in_response


async def get_today_lessons(telegram_id: int) -> list[any]:
    response = await get_request(path=f"/v3/users/{telegram_id}/timetables/today")
    await raise_schedule_exception_when_service_unavailable(response)

    data = response.json()

    await raise_user_not_found_exception_when_exception_in_response(data)

    return data if not has_error_in_response(data) else None


async def get_tomorrow_lessons(telegram_id: int) -> list[any] | None:
    response = await get_request(path=f"/v3/users/{telegram_id}/timetables/tomorrow")
    await raise_schedule_exception_when_service_unavailable(response)

    data = response.json()

    await raise_user_not_found_exception_when_exception_in_response(data)

    return data if not has_error_in_response(data) else None


async def get_timetables(telegram_id: int) -> dict[str, any] | None:
    response = await get_request(path=f"/v3/users/{telegram_id}/timetables")
    await raise_schedule_exception_when_service_unavailable(response)

    data = response.json()
    return data if not has_error_in_response(data) else None


async def get_timetable(telegram_id: int, id: str) -> dict[str, any]:
    response = await get_request(path=f"/v3/users/{telegram_id}/timetables/{id}")
    await raise_schedule_exception_when_service_unavailable(response)

    data = response.json()

    await raise_user_not_found_exception_when_exception_in_response(data)

    return data if not has_error_in_response(data) else None