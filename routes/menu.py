from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from decorator.decorators import typing_action, exception_handler

router = Router()


@router.message(Command('help', 'menu'))
@router.message(lambda F: F.text == ('help' or 'помощь' or 'помоги'))
@typing_action
@exception_handler
async def get_help(message: types.Message, state: FSMContext, is_need_delete: bool = True):
    await state.clear()

    if is_need_delete:
        await message.delete()
    text_help = ("<b>Вот, что я могу:</b>\n\n"
                 "🔹 /start — <i>Начало работы. Производится выбор курса, направления, группы и подгруппы</i>\n\n"
                 "🔹 /settings — <i>Изменение информации о себе</i>\n\n"
                 "🔹 /menu — <i>Получить меню для работы</i>\n\n"
                 "🔹 /schedule — <i>Получить расписание</i>\n\n"
                 "🔹 /base_schedule — <i>Получить расписание на модуль</i>\n\n"
                 "🔹 /sport_schedule — <i>Получить расписание физ-ры</i>\n\n"
                 "❗ При удалении этого сообщения кнопки выбора расписания пропадут. "
                 "Чтобы их вернуть, введи /menu еще раз! 🙂")

    keyboard_markup_up = ReplyKeyboardBuilder()
    get_schedule_text_button = types.KeyboardButton(text="💼 Расписание на неделю")
    get_base_schedule_text_button = types.KeyboardButton(text="🗓 Расписание на модуль")

    keyboard_markup_up.row(get_schedule_text_button)
    keyboard_markup_up.row(types.KeyboardButton(text="📅 На сегодня"), types.KeyboardButton(text="➡️ На завтра"))
    keyboard_markup_up.row(get_base_schedule_text_button, types.KeyboardButton(text="🏓 Расписание физ-ры"))
    keyboard_markup_up.row(types.KeyboardButton(text="⚙️ Настройки"))
    keyboard_markup_up.row(types.KeyboardButton(text="⚡️ Быстрый VPN от Вышкинцев"))
    keyboard_markup_up.row_width = 4

    keyboard = keyboard_markup_up.as_markup()
    keyboard.resize_keyboard = True

    await message.answer(text_help, reply_markup=keyboard, parse_mode='HTML')
