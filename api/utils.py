import requests

import venv

from requests import Response

from exception.schedule_service_unavailable_exception import ScheduleServiceUnavailableException
from exception.user_not_found_exception import UserNotFoundException


base_url = venv.base_url
x_secret_key = venv.x_secret_key
accept_data = "application/json"
required_headers = {"X-Secret-Key": x_secret_key, "Accept": accept_data,
                    "Content-Type": "application/json; charset=utf-8"}


async def get_request_as_json(path: str, headers: dict[str, str] = {}) -> dict[str, any]:
    """
    Get request as json from backend
    :param path api path for request
    :param headers for request, without required
    :return: get response as json
    """
    response = await get_request(path, headers)
    return response.json()


async def get_request(path: str, headers: dict[str, str] = {}) -> requests.Response:
    """
    Get request from backend
    :param path api path for request
    :param headers for request, without required
    :return: get response as response object
    """
    return requests.get(
        url=f"{base_url}{path}",
        headers=headers | required_headers
    )


async def post_request_as_json(path: str, headers: dict[str, str] = {}, json: dict[str, any] = None) -> dict[str, any]:
    """
    Post request as json from backend
    :param path api path for request
    :param headers for request, without required
    :param json payload for request
    :return: get response as json
    """
    response = await post_request(path, headers, json)
    return response.json()


async def post_request(path: str, headers: dict[str, str] = {}, json: dict[str, any] = None) -> requests.Response:
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
        headers=headers | required_headers
    )


async def patch_request_as_json(path: str, headers: dict[str, str] = {}, json: dict[str, any] = None) -> dict[str, any]:
    """
    Patch request as json from backend
    :param path api path for request
    :param headers for request, without required
    :param json payload for request
    :return: get response as json
    """
    response = await patch_request(path, headers, json)
    return response.json()


async def patch_request(path: str, headers: dict[str, str] = {}, json: dict[str, any] = None) -> requests.Response:
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
        headers=headers | required_headers
    )


async def delete_request_as_json(path: str, headers: dict[str, str] = {}, json: dict[str, any] = None) -> dict[
    str, any]:
    """
    Delete request as json from backend
    :param path api path for request
    :param headers for request, without required
    :return: delete response as json
    """
    response = await delete_request(path, headers, json)
    return response.json()


async def delete_request(path: str, headers: dict[str, str] = {}, json: dict[str, any] = None) -> requests.Response:
    """
    Delete request from backend
    :param path api path for request
    :param headers for request, without required
    :return: delete response as response object
    """
    return requests.delete(
        url=f"{base_url}{path}",
        headers=headers | required_headers,
        json=json
    )


async def raise_schedule_exception_when_service_unavailable(response: Response):
    if response.status_code == 503:
        raise ScheduleServiceUnavailableException


async def raise_user_not_found_exception_when_exception_in_response(data):
    if data["error"]:
        if data["errorDescription"]["code"] == "UserNotFoundException":
            raise UserNotFoundException