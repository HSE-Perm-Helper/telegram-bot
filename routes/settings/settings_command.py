from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import callback.callback
from decorator.decorators import typing_action
from routes import registration
from routes.settings.email_settings import router as email_router
from routes.settings.hiding_lessons_settings import router as hiding_lessons_router
from routes.settings.notification_settings import router as notification_router
from routes.settings.shared import SettingsCallback, __get_settings_keyboard

router = Router()

router.include_routers(
    notification_router,
    hiding_lessons_router,
    email_router
)


@router.message(Command('settings', 'настройки'))
@router.message(F.text == "⚙️ Настройки")
@typing_action
async def get_settings(message: Message, state: FSMContext):
    await state.clear()

    await message.delete()
    text = "⚙️ Настройки"
    keyboard = await __get_settings_keyboard()
    await message.answer(text, reply_markup=keyboard.as_markup())


@router.callback_query(lambda c: callback.callback.check_callback(c, SettingsCallback.DONE_SETTINGS.value))
async def done_settings(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.delete()


@router.callback_query(lambda c: callback.callback.check_callback(c, SettingsCallback.SET_GROUP.value))
async def change_group(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await state.clear()
    await registration.get_course(query.message, False)