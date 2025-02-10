import dataclasses

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.data_service import DataField, data_service
from decorator.decorators import typing_action, required_admin
from util.utils import parse_boolean

router = Router()

class AdminSettingsState(StatesGroup):
    OPENED_SETTINGS = State()

@dataclasses.dataclass()
class AdminSettings:
    name: str
    key: str


def _get_settings() -> list[AdminSettings]:
    return [
        AdminSettings("Проверка уведомлений", DataField.IS_ENABLED_NOTIFICATIONS_FETCH.value),
        AdminSettings("Проверка работы бэка", DataField.IS_ENABLED_BACKEND_HEALTH_CHECK.value)
    ]

@router.message(Command("bot_settings"))
@typing_action
@required_admin
async def bot_settings_command(message: Message, state: FSMContext):
    await state.clear()

    await message.delete()
    text = "⚙️ Настройки бота"
    keyboard = await __get_settings_keyboard()
    await message.answer(text, reply_markup=keyboard.as_markup())
    await state.set_state(AdminSettingsState.OPENED_SETTINGS)


async def __get_settings_keyboard():
    keyboard = InlineKeyboardBuilder()

    for setting in _get_settings():
        value = parse_boolean(await data_service.get_data(setting.key))
        keyboard.row(InlineKeyboardButton(text=f"{__get_state_for_setting(value)} {setting.name}", callback_data=setting.key))

    keyboard.row(InlineKeyboardButton(text="Готово", callback_data="done"))
    return keyboard


@router.callback_query(AdminSettingsState.OPENED_SETTINGS)
async def process_setting(query: CallbackQuery, state: FSMContext):
    await query.answer()
    if query.data == "done":
        await state.clear()
        await query.message.delete()
        return

    for setting in _get_settings():
        if setting.key == query.data:
            value = parse_boolean(await data_service.get_data(setting.key))
            new_value = not value
            await data_service.set_data(setting.key, new_value)
            keyboard = await __get_settings_keyboard()
            await query.message.edit_reply_markup(reply_markup=keyboard.as_markup())
            break


def __get_state_for_setting(value: bool) -> str:
    symbol = "✅"
    if not value:
        symbol = "❌"
    return symbol

