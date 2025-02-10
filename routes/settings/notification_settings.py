from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback.callback import extract_data_from_callback, check_callback
from settings.setting_code import SettingCode
from settings.base_setting import BaseSetting
from settings.settings_service import settings_service
from routes.settings.shared import SettingsState, SettingsCallback, back_to_settings

router = Router()

@router.callback_query(lambda c: check_callback(c, SettingsCallback.NOTIFICATION_SETTINGS.value))
async def notification_settings(query: CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardBuilder()
    settings: list[SettingCode] = [SettingCode.NEW_SCHEDULE_NOTIFICATION, SettingCode.CHANGED_SCHEDULE_NOTIFICATION,
                                   SettingCode.COMING_LESSONS_NOTIFICATION]

    settings = await settings_service.get_settings(query.message.chat.id, settings)

    for data, value in settings:
        data: BaseSetting
        value: bool

        keyboard.row(await __get_inline_button_for_setting(data, value))

    keyboard.row(InlineKeyboardButton(text="⬅️ В настройки", callback_data="back"))
    await state.set_state(SettingsState.CHANGE_NOTIFICATION_SETTING)
    await query.message.edit_reply_markup(reply_markup=keyboard.as_markup())


@router.callback_query(SettingsState.CHANGE_NOTIFICATION_SETTING)
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


@router.callback_query(lambda c: check_callback(c, SettingsCallback.OFF_NOTIFICATION.value))
async def disable_notification(query: CallbackQuery):
    await query.message.delete()

    code = SettingCode(
        extract_data_from_callback(SettingsCallback.OFF_NOTIFICATION.value, query.data)[0])

    setting = await settings_service.get_setting_by_code(code)
    setting_title = setting.title

    await settings_service.toggle_setting(query.message.chat.id, code, new_value=False)

    await query.answer(text=f"✅ Вы успешно отключили {setting_title.lower()}")


async def __get_inline_button_for_setting(data: BaseSetting, value: bool) -> InlineKeyboardButton:
    symbol = "✅"
    if not value:
        symbol = "❌"
    return InlineKeyboardButton(text=f"{symbol} {data.title}", callback_data=f"{data.code.value}_{value}")