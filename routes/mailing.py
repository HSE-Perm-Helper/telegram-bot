from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from api import user_service, schedule_service
from constants import constant
from decorator.decorators import required_admin, typing_action
from util.users_utils import send_message_to_users

router = Router()


class MailingState(StatesGroup):
    waiting_mailing_target_course = State()
    waiting_mailing_target_program = State()
    waiting_mailing_target_group = State()
    waiting_mailing_message = State()


@router.message(Command("mailing"))
@required_admin
async def mailing_to_all(message: Message, state: FSMContext):
    await state.clear()

    courses = await schedule_service.get_courses()
    keyboard = InlineKeyboardBuilder()
    text = "Выберите курсы, в которые необходимо сделать рассылку:"
    for i in range(len(courses)):
        emoji_for_button = f"{constant.emojies_for_course[i]} {courses[i]} курс"
        keyboard.row(types.InlineKeyboardButton(text=emoji_for_button,
                                                callback_data=f"{courses[i]}"))
    keyboard.row(types.InlineKeyboardButton(text="Не важно",
                                            callback_data="all"))

    await message.answer(text=text, reply_markup=keyboard.as_markup())
    await state.set_state(MailingState.waiting_mailing_target_course)


@typing_action
@router.callback_query(StateFilter(MailingState.waiting_mailing_target_course))
async def callback_message(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data
    course = None

    await state.update_data(course=course)

    if data != "all":
        course = int(data)

        keyboard = InlineKeyboardBuilder()
        programs = await schedule_service.get_programs(course)

        for program in programs:
            keyboard.row(InlineKeyboardButton(text=program, callback_data=f"{program}"))

        keyboard.row(InlineKeyboardButton(text="Не важно", callback_data="all"))

        await callback_query.message.edit_text("Выберите программу, для которой сделать рассылку:")
        await callback_query.message.edit_reply_markup(reply_markup=keyboard.as_markup())

        await state.update_data(course=course)
        await state.set_state(MailingState.waiting_mailing_target_program)
    else:
        await next_step_for_mailing_message(callback_query, state)


@typing_action
@router.callback_query(StateFilter(MailingState.waiting_mailing_target_program))
async def callback_message(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data
    program = None

    await state.update_data(program=program)

    if data == "all":
        return await next_step_for_mailing_message(callback_query, state)

    program = str(data)
    data = await state.get_data()
    course = data.get("course")

    keyboard = InlineKeyboardBuilder()
    groups = await schedule_service.get_groups(course, program)

    for group in groups:
        keyboard.row(InlineKeyboardButton(text=group, callback_data=f"{group}"))

    keyboard.row(InlineKeyboardButton(text="Не важно", callback_data="all"))

    await callback_query.message.edit_text("Выберите группу, для которой сделать рассылку:")
    await callback_query.message.edit_reply_markup(reply_markup=keyboard.as_markup())

    await state.update_data(program=program)
    await state.set_state(MailingState.waiting_mailing_target_group)


@typing_action
@router.callback_query(StateFilter(MailingState.waiting_mailing_target_group))
async def callback_message(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data
    group = None

    await state.update_data(group=group)

    if data == "all":
        return await next_step_for_mailing_message(callback_query, state)

    group = str(data)
    await state.update_data(group=group)

    await next_step_for_mailing_message(callback_query, state)



async def next_step_for_mailing_message(query: CallbackQuery, state: FSMContext):
    await query.message.delete()

    await query.message.answer(
        "Введите сообщение для рассылки: ")
    await state.set_state(MailingState.waiting_mailing_message)


@router.message(F.text, MailingState.waiting_mailing_message)
@typing_action
async def send_mail(message: Message, state: FSMContext):
    data = await state.get_data()

    course = data.get("course")
    program = data.get("program")
    group = data.get("group")

    users = await user_service.filter_user_ids(course, program, group)
    actual, expected = await send_message_to_users(message.html_text, users)
    await state.clear()

    await message.answer(f"Рассылка успешно отправлена! Всего попыток – {expected}, успешно – {actual}")
