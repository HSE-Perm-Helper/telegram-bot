from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

import callback.callback
from api import user_service, schedule_service
from callback.settings_callback import SettingsCallback
from decorator.decorators import typing_action
from exception.quarter_schedule_not_found_exception import QuarterScheduleNotFoundException
from message.settings_messages import HIDING_LESSONS_YET_UNAVAILABLE
from model.available_for_hiding_lesson import AvailableForHidingLesson
from routes import registration
from settings.base_setting import BaseSetting
from settings.setting_code import SettingCode
from settings.settings_service import settings_service

router = Router()


class SettingsState(StatesGroup):
    HIDING_LESSONS_SETTING = State()
    CHANGE_NOTIFICATION_SETTING = State()


@router.message(Command('settings', 'настройки'))
@router.message(F.text == "⚙️ Настройки")
@typing_action
async def get_settings(message: Message, state: FSMContext):
    await state.clear()

    await message.delete()
    text = "⚙️ Настройки"
    keyboard = await __get_settings_keyboard()
    await message.answer(text, reply_markup=keyboard.as_markup())


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


@router.callback_query(lambda c: callback.callback.check_callback(c, SettingsCallback.OFF_NOTIFICATION.value))
async def disable_notification(query: CallbackQuery):
    await query.message.delete()

    code = SettingCode(
        callback.callback.extract_data_from_callback(SettingsCallback.OFF_NOTIFICATION.value, query.data)[0])

    setting = await settings_service.get_setting_by_code(code)
    setting_title = setting.title

    await settings_service.toggle_setting(query.message.chat.id, code, new_value=False)

    await query.answer(text=f"✅ Вы успешно отключили {setting_title.lower()}")


@router.callback_query(lambda c: callback.callback.check_callback(c, SettingsCallback.DONE_SETTINGS.value))
async def done_settings(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.delete()


@router.callback_query(lambda c: callback.callback.check_callback(c, SettingsCallback.SET_GROUP.value))
async def change_group(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await state.clear()
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


@router.callback_query(F.data == SettingsCallback.HIDING_LESSONS_SETTINGS.value)
async def hiding_lessons_settings(query: CallbackQuery, state: FSMContext):
    try:
        data = await schedule_service.get_available_for_hiding_lessons(query.message.chat.id)
    except QuarterScheduleNotFoundException as e:
        await query.message.answer(HIDING_LESSONS_YET_UNAVAILABLE)
        return

    hidden_lessons = await user_service.get_user_hidden_lessons(query.message.chat.id)
    hidden_lessons = set(
        map(lambda lesson: AvailableForHidingLesson(lesson.lesson, lesson.lesson_type, lesson.sub_group),
            hidden_lessons))

    values = []

    for lesson in data:
        if lesson in hidden_lessons:
            values.append(True)
        else:
            values.append(False)

    await query.message.edit_text("Выберите предметы, которые хотите скрыть 👀")

    await state.update_data(lessons=data, values=values)
    await state.set_state(SettingsState.HIDING_LESSONS_SETTING)

    await show_hiding_lessons(query, state, 1)


async def show_hiding_lessons(query: CallbackQuery, state: FSMContext, page: int, count_by_page: int = 8):
    data = await state.get_data()

    lessons = data["lessons"]
    values = data["values"]

    keyboard = InlineKeyboardBuilder()

    start = (page - 1) * count_by_page
    end = min(len(lessons), start + count_by_page)

    for i in range(start, end):
        lesson = lessons[i]
        value = values[i]

        keyboard.row(await __get_hide_lesson_button(lesson, value, i))

    must_be_paged = False

    back_button = InlineKeyboardButton(text=" ", callback_data="none")
    if page > 1:
        back_button = InlineKeyboardButton(text="👈", callback_data=f"back_page{page - 1}")
        must_be_paged = True

    next_button = InlineKeyboardButton(text=" ", callback_data="none")
    if end < len(lessons):
        next_button = InlineKeyboardButton(text="👉", callback_data=f"next_page{page + 1}")
        must_be_paged = True
    if must_be_paged:
        keyboard.row(back_button, next_button)
    keyboard.row(InlineKeyboardButton(text="⬅️ В настройки", callback_data="back"))

    await query.message.edit_reply_markup(reply_markup=keyboard.as_markup())


async def __get_hide_lesson_button(lesson: AvailableForHidingLesson, value: bool, index: int) -> InlineKeyboardButton:
    text = ""
    if value:
        text = "✅ "
    if lesson.sub_group:
        text += f"{lesson.lesson_type.short_name.capitalize()} {lesson.sub_group} пг | {lesson.lesson}"
    else:
        text += f"{lesson.lesson_type.short_name.capitalize()} | {lesson.lesson}"

    return InlineKeyboardButton(text=text, callback_data=f"{index}")


@router.callback_query(SettingsState.HIDING_LESSONS_SETTING)
async def hiding_lessons_handle(query: CallbackQuery, state: FSMContext):
    if query.data == "none":
        await query.answer()
        return

    if query.data == "back":
        return await back_to_settings(query, state)

    if query.data.startswith("next_page"):
        page = int(query.data.replace("next_page", ""))
        await show_hiding_lessons(query, state, page)
        return

    if query.data.startswith("back_page"):
        page = int(query.data.replace("back_page", ""))
        await show_hiding_lessons(query, state, page)
        return

    index = int(query.data)

    data = await state.get_data()
    lessons: list[AvailableForHidingLesson] = data["lessons"]
    values = data["values"]

    lesson = lessons[index]

    if not values[index]:
        await user_service.add_user_hidden_lesson(query.message.chat.id, lesson)
        await query.answer(f"✅ Вы успешно добавили в скрытые предмет {lesson.lesson}!")
    else:
        await user_service.remove_user_hidden_lesson(query.message.chat.id, lesson)
        await query.answer(f"✅ Вы успешно убрали из скрытых предмет {lesson.lesson}!")

    values[index] = not values[index]
    await state.update_data(values=values)

    new_keyboard = []

    for row in query.message.reply_markup.inline_keyboard:
        if row[0].callback_data == query.data:
            new_keyboard.append([await __get_hide_lesson_button(lesson, values[index], index)])
        else:
            new_keyboard.append(row)

    await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=new_keyboard))


async def __get_inline_button_for_setting(data: BaseSetting, value: bool) -> InlineKeyboardButton:
    symbol = "✅"
    if not value:
        symbol = "❌"
    return InlineKeyboardButton(text=f"{symbol} {data.title}", callback_data=f"{data.code.value}_{value}")
