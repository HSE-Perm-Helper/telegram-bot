from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

import callback.callback
from callback.settings_callback import SettingsCallback
from decorator.decorators import typing_action, exception_handler
from routes import registration
from settings.base_setting import BaseSetting
from settings.setting_code import SettingCode
from settings.settings_service import settings_service

router = Router()


class SettingsState(StatesGroup):
    CHANGE_SETTING = State()


@router.message(Command('settings', 'настройки'))
@router.message(F.text == "⚙️ Настройки")
@typing_action
@exception_handler
async def get_settings(message: Message, state: FSMContext):
    await state.clear()

    await message.delete()
    text = "⚙️ Настройки"
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="📚 Группа", callback_data=SettingsCallback.SET_GROUP.value))
    keyboard.row(InlineKeyboardButton(text="🔔 Уведомления", callback_data=SettingsCallback.NOTIFICATION_SETTINGS.value))
    keyboard.row(InlineKeyboardButton(text="✅ Готово ✅", callback_data=SettingsCallback.DONE_SETTINGS.value))
    await message.answer(text, reply_markup=keyboard.as_markup())


async def back_to_settings(query: CallbackQuery, state: FSMContext):
    await state.clear()
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="📚 Группа", callback_data=SettingsCallback.SET_GROUP.value))
    keyboard.row(InlineKeyboardButton(text="🔔 Уведомления", callback_data=SettingsCallback.NOTIFICATION_SETTINGS.value))
    keyboard.row(InlineKeyboardButton(text="✅ Готово ✅", callback_data=SettingsCallback.DONE_SETTINGS.value))
    await query.message.edit_reply_markup(reply_markup=keyboard.as_markup())



@router.callback_query(lambda c: callback.callback.check_callback(c, SettingsCallback.OFF_NOTIFICATION.value))
async def disable_notification(query: CallbackQuery):
    await query.message.delete()

    code = SettingCode(callback.callback.extract_data_from_callback(SettingsCallback.OFF_NOTIFICATION.value, query.data)[0])

    setting = await settings_service.get_setting_by_code(code)
    setting_title = setting.title

    await settings_service.toggle_setting(query.message.chat.id, code, new_value=False)

    await query.answer(text=f"✅ Вы успешно отключили {setting_title.lower()}")


@router.callback_query(lambda c: callback.callback.check_callback(c, SettingsCallback.DONE_SETTINGS.value))
async def done_settings(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.delete()

@router.callback_query(lambda c: callback.callback.check_callback(c, SettingsCallback.SET_GROUP.value))
async def change_group(query: CallbackQuery):
    await registration.get_course(query.message, False)


@router.callback_query(lambda c: callback.callback.check_callback(c, SettingsCallback.NOTIFICATION_SETTINGS.value))
async def notification_settings(query: CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardBuilder()
    settings: list[SettingCode] = [SettingCode.NEW_SCHEDULE_NOTIFICATION, SettingCode.CHANGED_SCHEDULE_NOTIFICATION,
                                   SettingCode.COMING_LESSONS_NOTIFICATION]

    settings = await settings_service.get_settings(query.message.chat.id, settings)

    for data, value in settings:
        data: BaseSetting
        value: bool

        keyboard.row(await __get_inline_button_for_setting(data, value))

    keyboard.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="back"))
    await state.set_state(SettingsState.CHANGE_SETTING)
    await query.message.edit_reply_markup(reply_markup=keyboard.as_markup())


@router.callback_query(SettingsState.CHANGE_SETTING)
async def change_state(query: CallbackQuery, state: FSMContext):
    if query.data == "back":
        return await back_to_settings(query, state)

    value = query.data.split("_")[-1]
    new_state = True

    if value == "True":
        new_state = False

    new_keyboard = []

    code = SettingCode("_".join(query.data.split("_")[:-1]))

    await settings_service.toggle_setting(query.message.chat.id, code, new_value=new_state)

    setting = await settings_service.get_setting_by_code(code)
    setting_title = setting.title

    for row in query.message.reply_markup.inline_keyboard:
        if row[0].callback_data == query.data:
            new_keyboard.append([await __get_inline_button_for_setting(setting, new_state)])
        else:
            new_keyboard.append(row)

    await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=new_keyboard))

    if new_state:
        await query.answer(f"✅ Вы успешно включили {setting_title.lower()}")
    else:
        await query.answer(f"✅ Вы успешно отключили {setting_title.lower()}")



async def __get_inline_button_for_setting(data: BaseSetting, value: bool) -> InlineKeyboardButton:
    symbol = "✅"
    if not value:
        symbol = "❌"
    return InlineKeyboardButton(text=f"{symbol} {data.title}", callback_data=f"{data.code.value}_{value}")


