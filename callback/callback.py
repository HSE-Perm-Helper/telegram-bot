from aiogram import types

CALLBACK_DELIMITER = ":"


def extract_data_from_callback(callback_prefix: str, callback: str) -> list[str]:
    return callback.replace(callback_prefix + CALLBACK_DELIMITER, "", 1).split(CALLBACK_DELIMITER)


def insert_data_to_callback(callback_prefix: str, data: list) -> str:
    return callback_prefix + CALLBACK_DELIMITER + CALLBACK_DELIMITER.join(list(map(str, data)))


def check_callback(callback: types.CallbackQuery, target_callback: str) -> bool:
    return callback.data.startswith(target_callback)
