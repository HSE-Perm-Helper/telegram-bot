from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from api import user_service
from decorator.decorators import typing_action
from routes import menu, registration

router = Router()


@router.message(Command('start', 'старт', 'поехали', 'registration', 'регистрация'))
@router.message(lambda F: F.text == ('start' or 'старт' or 'поехали'
                                     or 'registration' or 'регистрация'))
@typing_action
async def get_registration(message: Message, state: FSMContext):
    await state.clear()

    if await user_service.check_registration_user(message.chat.id):
        await menu.send_help_message(message)
    else:
        await registration.get_course(message, True)
