import requests

import venv

base_url = venv.base_url
x_secret_key = venv.x_secret_key
accept_data = "application/json"
required_headers = {"X-Secret-Key": x_secret_key, "Accept": accept_data,
                    "Content-Type": "application/json; charset=utf-8"}


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


def delete_request_as_json(path: str, headers: dict[str, str] = {}) -> dict[str, any]:
    """
    Delete request as json from backend
    :param path api path for request
    :param headers for request, without required
    :return: delete response as json
    """
    return (delete_request(path, headers)
            .json())


def delete_request(path: str, headers: dict[str, str] = {}) -> requests.Response:
    """
    Delete request from backend
    :param path api path for request
    :param headers for request, without required
    :return: delete response as response object
    """
    return requests.delete(
        url=f"{base_url}{path}",
        headers=headers | required_headers,
        verify=False
    )
