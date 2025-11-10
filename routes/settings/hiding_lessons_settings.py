from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from api import user_settings_service
from exception.quarter_schedule_not_found_exception import QuarterScheduleNotFoundException
from message.settings_messages import HIDING_LESSONS_YET_UNAVAILABLE
from model.available_for_hiding_lesson import AvailableForHidingLesson
from routes.settings.shared import SettingsState, SettingsCallback, back_to_settings

router = Router()

@router.callback_query(F.data == SettingsCallback.HIDING_LESSONS_SETTINGS.value)
async def hiding_lessons_settings(query: CallbackQuery, state: FSMContext):
    try:
        data = await user_settings_service.get_available_for_hiding_lessons(query.message.chat.id)
    except QuarterScheduleNotFoundException as e:
        await query.message.answer(HIDING_LESSONS_YET_UNAVAILABLE)
        return

    hidden_lessons = await user_settings_service.get_user_hidden_lessons(query.message.chat.id)
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
    converted_data = list(map(lambda lesson: lesson.to_dict(), data))
    await state.update_data(lessons=converted_data, values=values)
    await state.set_state(SettingsState.HIDING_LESSONS_SETTING)

    await show_hiding_lessons(query, state, 1)


async def show_hiding_lessons(query: CallbackQuery, state: FSMContext, page: int, count_by_page: int = 8):
    data = await state.get_data()

    lessons = from_dict_list_to_lessons(data["lessons"])
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
    lessons: list[AvailableForHidingLesson] = from_dict_list_to_lessons(data["lessons"])
    values = data["values"]

    lesson = lessons[index]

    if not values[index]:
        await user_settings_service.add_user_hidden_lesson(query.message.chat.id, lesson)
        await query.answer(f"✅ Вы успешно добавили в скрытые предмет {lesson.lesson}!")
    else:
        await user_settings_service.remove_user_hidden_lesson(query.message.chat.id, lesson)
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


def from_dict_list_to_lessons(l: list[dict]) -> list[AvailableForHidingLesson]:
    return list(map(lambda lesson: AvailableForHidingLesson.from_dict(lesson), l))