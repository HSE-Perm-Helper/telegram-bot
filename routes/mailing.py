from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder

from api import api
from constants import constant
from decorator.decorators import required_admin, typing_action
from util.users_utils import send_message_to_users

router = Router()


class MailingState(StatesGroup):
    waiting_mailing_target = State()
    waiting_mailing_message = State()


@router.message(Command("mailing"))
@required_admin
async def mailing_to_all(message: types.Message, state: FSMContext):
    await state.clear()

    courses = await api.get_courses()
    keyboard = InlineKeyboardBuilder()
    text = "Выберите курсы, в которые необходимо сделать рассылку:"
    for i in range(len(courses)):
        emoji_for_button = f"{constant.emojies_for_course[i]} {courses[i]} курс"
        keyboard.row(types.InlineKeyboardButton(text=emoji_for_button,
                                                callback_data=f"{courses[i]}"))
    keyboard.row(types.InlineKeyboardButton(text="Всем",
                                            callback_data="all"))

    await message.answer(text=text, reply_markup=keyboard.as_markup())
    await state.set_state(MailingState.waiting_mailing_target)


@typing_action
@router.callback_query(StateFilter(MailingState.waiting_mailing_target))
async def callback_message(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    data = callback_query.data
    course = None
    if data != "all":
        course = int(data)
    await callback_query.message.answer(
        "Введите сообщение для рассылки: ")
    await state.set_state(MailingState.waiting_mailing_message)
    await state.update_data(course=course)


@router.message(F.text, MailingState.waiting_mailing_message)
@typing_action
async def send_mail(message: types.Message, state: FSMContext):
    data = await state.get_data()
    course = data.get("course")

    await message.answer("Рассылка успешно отправлена!")
    if not course:
        users = await api.get_user_ids()
    else:
        users = await api.get_user_ids_by_course(course)
    await send_message_to_users(message.html_text, users)
    await state.clear()
