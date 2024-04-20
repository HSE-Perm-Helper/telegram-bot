import datetime

import requests

import venv

import api

base_url = venv.base_url
x_secret_key = venv.x_secret_key
accept_data = "application/json"
required_headers = {"X-Secret-Key": x_secret_key, "Accept": accept_data,
                    "Content-Type": "application/json; charset=utf-8"}

days_of_week_list = ['Понедельник',
                     'Вторник',
                     'Среда',
                     'Четверг',
                     'Пятница',
                     'Суббота',
                     'Воскресенье']

days_of_week_slug = {
    "MONDAY": days_of_week_list[0],
    "TUESDAY": days_of_week_list[1],
    "WEDNESDAY": days_of_week_list[2],
    "THURSDAY": days_of_week_list[3],
    "FRIDAY": days_of_week_list[4],
    "SATURDAY": days_of_week_list[5],
    "SUNDAY": days_of_week_list[6]
}


def get_request_as_json(path: str, headers: dict[str, str] = {}) -> dict[str, any]:
    """
    Get request as json from backend
    :param path api path for request
    :param headers for request, without required
    :return: get response as json
    """
    return (get_request(path, headers)
            .json())


def get_request(path: str, headers: dict[str, str] = {}) -> requests.Response:
    """
    Get request from backend
    :param path api path for request
    :param headers for request, without required
    :return: get response as response object
    """
    return requests.get(
        url=f"{base_url}{path}",
        headers=headers | required_headers,
        verify=False
    )


def post_request_as_json(path: str, headers: dict[str, str] = {}, json: dict[str, any] = None) -> dict[str, any]:
    """
    Post request as json from backend
    :param path api path for request
    :param headers for request, without required
    :param json payload for request
    :return: get response as json
    """
    return (post_request(path, headers, json)
            .json())


def post_request(path: str, headers: dict[str, str] = {}, json: dict[str, any] = None) -> requests.Response:
    """
    Post request from backend
    :param path api path for request
    :param headers for request, without required
    :param json payload for request
    :return: post response as response object
    """
    return requests.post(
        url=f"{base_url}{path}",
        json=json,
        headers=headers | required_headers,
        verify=False
    )


def patch_request_as_json(path: str, headers: dict[str, str] = {}, json: dict[str, any] = None) -> dict[str, any]:
    """
    Patch request as json from backend
    :param path api path for request
    :param headers for request, without required
    :param json payload for request
    :return: get response as json
    """
    return (patch_request(path, headers, json)
            .json())


def patch_request(path: str, headers: dict[str, str] = {}, json: dict[str, any] = None) -> requests.Response:
    """
    Patch request from backend
    :param path api path for request
    :param headers for request, without required
    :param json payload for request
    :return: post response as response object
    """
    return requests.patch(
        url=f"{base_url}{path}",
        json=json,
        headers=headers | required_headers,
        verify=False
    )


def delete_request_as_json(path: str, headers: dict[str, str] = {}, json: dict[str, any] = None) -> dict[str, any]:
    """
    Delete request as json from backend
    :param path api path for request
    :param headers for request, without required
    :return: delete response as json
    """
    return (delete_request(path, headers, json)
            .json())


def delete_request(path: str, headers: dict[str, str] = {}, json: dict[str, any] = None) -> requests.Response:
    """
    Delete request from backend
    :param path api path for request
    :param headers for request, without required
    :return: delete response as response object
    """
    return requests.delete(
        url=f"{base_url}{path}",
        headers=headers | required_headers,
        json=json,
        verify=False
    )


def is_admin(telegram_id: int) -> bool:
    """
    Check user is admin
    :param telegram_id user telegram id
    :return True if user is admin
    """
    admins = api.get_admin_ids()
    return telegram_id in admins


def format_output_array(array: list[str]):
    if len(array) == 0:
        return ""
    if array[0] is not str:
        array = list(map(str, array))
    if len(array) == 1:
        return array[0]
    output = ", ".join(array[0: len(array) - 1])
    return f"{output} и {array[-1]}"


def get_day_of_week_from_date(date_string: str) -> str:
    day_, month, year = date_string.split('.')
    day_ = int(day_)
    month = int(month)
    year = int(year)
    date = datetime.datetime(year, month, day_)
    day_of_the_week = days_of_week_list[date.isoweekday() - 1]
    return day_of_the_week


def get_day_of_week_from_slug(slug: str) -> str:
    return days_of_week_slug.get(slug.upper(), "N/a")

