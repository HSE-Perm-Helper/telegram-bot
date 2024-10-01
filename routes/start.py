from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from api import api
from decorator.decorators import typing_action, exception_handler
from routes import menu, registration

router = Router()


@router.message(Command('start', 'старт', 'поехали', 'registration', 'регистрация'))
@router.message(lambda F: F.text == ('start' or 'старт' or 'поехали'
                                     or 'registration' or 'регистрация'))
@typing_action
@exception_handler
async def get_registration(message, state: FSMContext):
    await state.clear()

    if await api.check_registration_user(message.chat.id):
        await menu.get_help(message, state, is_need_delete=False)
    else:
        await registration.get_course(message, True)
