from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from api import api
from bot import bot
from constants import constant
from decorator.decorators import typing_action, exception_handler, required_admin
from routes.registration import registration
from routes.schedule_handle import schedule_handle
from schedule.schedule_type import ScheduleType

router = Router()


# Обработка команды /start и /registration
@router.message(Command('start', 'старт', 'поехали', 'registration', 'регистрация'))
@router.message(lambda F: F.text == ('start' or 'старт' or 'поехали'
                                     or 'registration' or 'регистрация'))
@typing_action
@exception_handler
async def get_registration(message):
    if await api.check_registration_user(message.chat.id):
        await schedule_handle.get_menu(message)
    else:
        await registration.get_course(message, True)


# Обработка команды /help
@router.message(Command('help', 'помощь', 'помоги'))
@router.message(lambda F: F.text == ('help' or 'помощь' or 'помоги'))
@typing_action
@exception_handler
async def get_help(message):
    await bot.delete_message(message.chat.id, message.message_id)
    text_help = ("<b>Вот, что я могу:</b>\n\n"
                 "🔹 /start — <i>Начало работы. Производится выбор курса, направления, группы и подгруппы</i>\n\n"
                 "🔹 /settings — <i>Изменение информации о себе</i>\n\n"
                 "🔹 /menu — <i>Получить меню для работы</i>\n\n"
                 "🔹 /schedule — <i>Получить расписание</i>\n\n"
                 "🔹 /base_schedule — <i>Получить расписание на модуль</i>\n\n"
                 "Канал для обратной связи — <b>@hse_perm_helper_feedback</b>\n"
                 "Будем рады твоему отзыву или предложению!\n\n"
                 f"Версия <i>{constant.version}</i>")
    await message.answer(text_help, parse_mode='HTML')


# Обработка команды /menu
@router.message(Command('menu', 'меню'))
@router.message(lambda F: F.text == ('menu' or 'меню'))
@typing_action
@exception_handler
async def start_working(message):
    await bot.delete_message(message.chat.id, message.message_id)
    await schedule_handle.get_menu(message)


# Обработка команды /settings
@router.message(Command('settings', 'настройки'))
@router.message(lambda F: F.text == ('settings' or 'настройки'))
@typing_action
@exception_handler
async def get_settings(message):
    await message.delete()
    await registration.get_course(message, False)


# Обработка команды /schedule
@router.message(Command('schedule', 'расписание'))
@router.message(lambda F: F.text == ('schedule' or 'расписание'))
@typing_action
@exception_handler
async def get_settings(message):
    await schedule_handle.get_text_schedule(message)


# Обработка сообщения добавления календаря
# @bot.message_handler(func= lambda message: message.text == "Добавить обновляемый календарь")
# def callback_message(message):
#     get_schedule(message)


# Обработка сообщения получения текстового расписания
@router.message(lambda
                        F: F.text == "Получить текстовое расписание 💼" or F.text == "Получить текстовое расписание")
@typing_action
@exception_handler
async def callback_message(message):
    await schedule_handle.get_text_schedule(message)


@router.message(Command('schedule'))
@typing_action
@exception_handler
@required_admin
async def get_remote_schedule(message):
    await bot.delete_message(message.chat.id, message.message_id)
    keyword = InlineKeyboardBuilder()
    link = await api.get_remote_schedule_link(message.chat.id)
    keyword.add(types.InlineKeyboardButton(text="Добавить расписание в календарь", url=link))
    await message.answer(text="Чтобы добавить расписание в свой календарь тебе всего лишь нужно нажать на кнопку и "
                              "выбрать календарь, который ты используешь."
                              "И всё. Твое расписание у тебя на устройстве!", reply_markup=keyword)


@router.message(Command("base_schedule"))
@router.message(lambda F: F.text == "Получить расписание на модуль 🗓")
@typing_action
@exception_handler
async def get_base_schedule(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    schedules_json = await api.get_schedules()
    schedules = list(filter(lambda schedule: schedule["scheduleType"] == ScheduleType.QUARTER_SCHEDULE.value,
                            schedules_json['response']))
    if len(schedules) == 0:
        await message.answer(text="Пока расписания на модуль нет! 🎉🎊")
    else:
        schedule = schedules[0]
        response_schedule = await api.get_schedule(message.chat.id, schedule["start"], schedule["end"])
        await schedule_handle.schedule_sending(message, response_schedule["response"])
