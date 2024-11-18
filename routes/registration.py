import random

from aiogram import Router, types
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from api import user_service, schedule_service
from constants import constant
from decorator.decorators import typing_action
from message.common_messages import SUCCESS_REGISTER, SUCCESS_DATA_CHANGING
from routes import menu

router = Router()


# Рандомный номер эмодзи для быстрого получения из списка
def rand_emj(count):
    return random.randint(0, count - 1)


# Создание кнопок выбора курса
async def get_course(message: Message, is_new_user: bool):
    if is_new_user:
        text_hello = "Давай познакомимся! 👋 На каком курсе ты учишься?"
    else:
        text_hello = "Немного изменим данные. ✏ На каком курсе ты учишься?"

    courses = await schedule_service.get_courses()
    random.shuffle(constant.emojies_for_course)

    keyboard = InlineKeyboardBuilder()

    for i in range(len(courses)):
        emoji_for_button = f"{constant.emojies_for_course[i]} {courses[i]} курс"
        keyboard.row(types.InlineKeyboardButton(text=emoji_for_button,
                                                callback_data=f"course_{courses[i]}"
                                                              f"^{is_new_user}"))

    await message.answer(text_hello, reply_markup=keyboard.as_markup())


# Создание кнопок выбора программы
async def get_program(message: Message, data):
    number_course, is_new_user = data.split('^')
    number_course = int(number_course)
    text_get_course = f"Ты выбрал {number_course} курс! 🎉 На каком направлении ты учишься?"
    random.shuffle(constant.emojies_for_programs)
    programs = await schedule_service.get_programs(number_course)

    keyboard = InlineKeyboardBuilder()

    for i in range(len(programs)):
        if programs[i] in constant.type_of_program_dict.keys():
            emoji_for_button = (f"{constant.emojies_for_programs[i]} "
                                f"{constant.type_of_program_dict[programs[i]]}")
        else:
            emoji_for_button = (f"{constant.emojies_for_programs[i]}"
                                f"{programs[i]}")
        keyboard.row(types.InlineKeyboardButton(text=emoji_for_button,
                                                callback_data=f"program_{programs[i]}"
                                                              f"^{number_course}"
                                                              f"^{is_new_user}"))
    keyboard.row(types.InlineKeyboardButton(text="⬅ Назад",
                                            callback_data=f"back_to_start{is_new_user}"))

    await message.answer(text_get_course, reply_markup=keyboard.as_markup())


# Создание кнопок выбора группы
async def get_group(message: Message, data):
    program, course, is_new_user = data.split('^')
    if program in constant.type_of_program_dict.keys():
        text_get_group = f"Отлично, ты выбрал: \n{constant.type_of_program_dict[program]} 😎\nТеперь давай выберем группу!"
    else:
        text_get_group = f"Отлично, ты выбрал {program} направление! 😎\nТеперь давай выберем группу!"
    random.shuffle(constant.emojies_for_groups)
    groups = await schedule_service.get_groups(course,
                                               program)

    keyboard = InlineKeyboardBuilder()
    for i in range(len(groups)):
        emoji_for_button = f"{constant.emojies_for_groups[i]} {groups[i]}"
        keyboard.row(types.InlineKeyboardButton(text=emoji_for_button,
                                                callback_data=f"group_{groups[i]}"
                                                              f"^{program}"
                                                              f"^{course}"
                                                              f"^{is_new_user}"))
    keyboard.row(types.InlineKeyboardButton(text="⬅ Назад",
                                            callback_data=f"back_to_program{course}"
                                                          f"^{is_new_user}"))

    await message.answer(text_get_group, reply_markup=keyboard.as_markup())


# Создание кнопок для подтверждения выбора
async def get_confirmation(message: Message, data):
    group, program, course, is_new_user = data.split('^')

    '''Заводим новую переменную номера группы, чтобы в сообщение выводилось полное название направления'''
    if program in constant.type_of_program_dict.keys():
        program_for_message = constant.type_of_program_dict[program]
    else:
        program_for_message = program

    text_confirmation = ("Отлично! ✅ Теперь давай проверим, всё ли верно:\n" +
                             f"{course}-й курс,\n"
                             f"{program_for_message},\n"
                             f"{group} — группа,"
                             f"\n\nВсе верно?")


    keyboard = InlineKeyboardBuilder()
    keyboard.row(types.InlineKeyboardButton(text="Все верно! 🎉🎊",
                                            callback_data=f"start_working{course}"
                                                          f"^{program}"
                                                          f"^{group}"
                                                          f"^{message.chat.id}"
                                                          f"^{is_new_user}"))
    keyboard.row(types.InlineKeyboardButton(text="Начать сначала ✏",
                                            callback_data=f"back_to_start"
                                                          f"{is_new_user}"))
    keyboard.row(types.InlineKeyboardButton(text="⬅ Назад",
                                            callback_data=f"back_to_group{program}"
                                                          f"^{course}"
                                                          f"^{is_new_user}"))

    await message.answer(text_confirmation, reply_markup=keyboard.as_markup())


# Обработка события нажатия на кнопку выбора курса
@typing_action
@router.callback_query(lambda c: c.data.startswith('course_'))
async def course_query_handler(callback_query: types.CallbackQuery):
    data = callback_query.data.replace("course_", "")
    await callback_query.message.delete()
    await get_program(callback_query.message, data)


# Обработка события нажатия на кнопку выбора программы
@typing_action
@router.callback_query(lambda c: c.data.startswith('program_'))
async def program_query_handler(callback_query: types.CallbackQuery):
    data = callback_query.data.replace("program_", "")
    await callback_query.message.delete()
    await get_group(callback_query.message, data)


# Обработка события нажатия на кнопку выбора группы
@typing_action
@router.callback_query(lambda c: c.data.startswith('group_'))
async def group_query_handler(callback_query: types.CallbackQuery):
    data = callback_query.data.replace("group_", "")
    await callback_query.message.delete()
    await get_confirmation(callback_query.message, data)


# Обработка события возврата на предыдущий выбор
@typing_action
@router.callback_query(lambda c: c.data.startswith('back_to_'))
async def program_query_handler(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    if callback_query.data.startswith('back_to_program'):
        data = callback_query.data.replace('back_to_program', "")
        await get_program(callback_query.message, data)
    elif callback_query.data.startswith('back_to_group'):
        data = callback_query.data.replace('back_to_group', "")
        await get_group(callback_query.message, data)
    elif callback_query.data.startswith('back_to_start'):
        data = callback_query.data.replace('back_to_start', "")
        await get_course(callback_query.message, data == "True")


# Обработка события нажатия на кнопку подтверждения данных
@typing_action
@router.callback_query(lambda c: c.data.startswith("start_working"))
async def callback_message(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    data = callback_query.data.replace('start_working', "")
    course, program, group, telegram_id, is_new_user = data.split("^")
    is_new_user = True if is_new_user == "True" else False

    if is_new_user:
        is_success = await user_service.registration_user(telegram_id=telegram_id,
                                                          group=group)
    else:
        is_success = await user_service.edit_user(telegram_id=telegram_id,
                                                  group=group)

    if is_success:
        if is_new_user:
            await callback_query.answer(text=SUCCESS_REGISTER)
        else:
            await callback_query.answer(text=SUCCESS_DATA_CHANGING)

        await menu.send_help_message(callback_query.message)

    else:
        await callback_query.message.answer("⚠ Произошла ошибка при внесении данных. 😔 "
                                            "Возможно, ты уже зарегистрирован 🙃\n"
                                            "Для изменения данных о себе введи команду "
                                            "/settings !")
