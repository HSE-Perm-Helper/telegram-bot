from aiogram import Router, F
from aiogram.filters import Command

from api import api
from decorator.decorators import typing_action, exception_handler
from routes import menu
from routes.registration import registration

router = Router()


@router.message(Command('start', 'старт', 'поехали', 'registration', 'регистрация'))
@router.message(lambda F: F.text == ('start' or 'старт' or 'поехали'
                                     or 'registration' or 'регистрация'))
@typing_action
@exception_handler
async def get_registration(message):
    if await api.check_registration_user(message.chat.id):
        await menu.get_help(message, is_need_delete=False)
    else:
        await registration.get_course(message, True)


@router.message(Command('settings', 'настройки'))
@router.message(F.text == "⚙️ Настройки")
@typing_action
@exception_handler
async def get_settings(message):
    await message.delete()
    await registration.get_course(message, False)
