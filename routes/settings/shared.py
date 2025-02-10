import enum

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class SettingsState(StatesGroup):
    HIDING_LESSONS_SETTING = State()
    CHANGE_NOTIFICATION_SETTING = State()


class SettingsCallback(enum.Enum):
    SET_GROUP = "SET_GROUP_SETTINGS"
    NOTIFICATION_SETTINGS = "NOTIFICATION_SETTINGS"
    HIDING_LESSONS_SETTINGS = "HIDING_LESSONS_SETTINGS"
    DONE_SETTINGS = "DONE_SETTINGS"
    OFF_NOTIFICATION = "OFF_NOTIFICATION"


async def back_to_settings(query: CallbackQuery, state: FSMContext):
    await state.clear()
    keyboard = await __get_settings_keyboard()
    await query.message.edit_text("⚙️ Настройки")
    await query.message.edit_reply_markup(reply_markup=keyboard.as_markup())


async def __get_settings_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="📚 Группа", callback_data=SettingsCallback.SET_GROUP.value))
    keyboard.row(
        InlineKeyboardButton(text="👁️ Скрытие предметов", callback_data=SettingsCallback.HIDING_LESSONS_SETTINGS.value))
    keyboard.row(InlineKeyboardButton(text="🔔 Уведомления", callback_data=SettingsCallback.NOTIFICATION_SETTINGS.value))
    keyboard.row(InlineKeyboardButton(text="✅ Готово ✅", callback_data=SettingsCallback.DONE_SETTINGS.value))
    return keyboard