from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from api import user_service
from decorator.decorators import typing_action, required_admin

router = Router()


# @router.message(Command("test"))
# async def test(message: types.Message, state: FSMContext):
#     keyboard = ReplyKeyboardBuilder()
#
#     keyboard.row(KeyboardButton(text="test Select People", callback_data="132",
#                                       request_users=KeyboardButtonRequestUsers(request_id=123, request_username=True, max_quantity=1)))
#     await message.answer("Выбери чела", reply_markup=keyboard.as_markup())
#
# @router.message(F.content_type == ContentType.USER_SHARED)
# async def test2(message: Message, state: FSMContext):
#     await message.answer("123")
#     #print(message.users_shared.users[0].username)


@router.message(Command('help', 'menu'))
@router.message(lambda F: F.text == ('help' or 'помощь' or 'помоги'))
@typing_action
async def get_help(message: types.Message, state: FSMContext):
    await state.clear()
    await message.delete()

    await send_help_message(message)


@typing_action
async def send_help_message(message: types.Message):
    text_help = ("<b>Вот, что я могу:</b>\n\n"
                 "🔹 /start — <i>Начало работы. Производится выбор курса, направления, группы и подгруппы</i>\n\n"
                 "🔹 /settings — <i>Изменение информации о себе</i>\n\n"
                 "🔹 /menu — <i>Получить меню для работы</i>\n\n"
                 "🔹 /schedule — <i>Получить расписание</i>\n\n"
                 "🔹 /base_schedule — <i>Получить расписание на модуль</i>\n\n"
                 "🔹 /sport_schedule — <i>Получить расписание физ-ры</i>\n\n"
                 "🔹 /today — <i>Получить расписание на сегодня</i>\n\n"
                 "🔹 /tomorrow — <i>Получить расписание на завтра</i>\n\n"
                 "❗ При удалении этого сообщения кнопки выбора расписания пропадут. "
                 "Чтобы их вернуть, введи /menu еще раз! 🙂")

    keyboard_markup_up = ReplyKeyboardBuilder()
    get_schedule_text_button = types.KeyboardButton(text="💼 Расписание на неделю")
    get_base_schedule_text_button = types.KeyboardButton(text="🗓 Расписание на модуль")

    keyboard_markup_up.row(get_schedule_text_button)
    keyboard_markup_up.row(types.KeyboardButton(text="📅 На сегодня"), types.KeyboardButton(text="➡️ На завтра"))
    keyboard_markup_up.row(get_base_schedule_text_button, types.KeyboardButton(text="🏓 Расписание физ-ры"))
    keyboard_markup_up.row(types.KeyboardButton(text="🖥️ Добавить в календарь"), types.KeyboardButton(text="⚙️ Настройки"))
    keyboard_markup_up.row(types.KeyboardButton(text="⚡️ Быстрый VPN от Вышкинцев"), types.KeyboardButton(text="💳 Поддержать разработчиков"))
    keyboard_markup_up.row_width = 4

    keyboard = keyboard_markup_up.as_markup()
    keyboard.resize_keyboard = True

    await message.answer(text_help, reply_markup=keyboard, parse_mode='HTML')


@required_admin
@router.message(Command("update_test"))
async def update_test(message: types.Message):
    text = ("* Наконец мы доделали это * 🎉\n\n"
            "Теперь вы можете легко добавить ваше расписание в календарь на мобильном устройстве 📱 или ПК 💻"
            "Это значит, что вы сможете всегда быть в курсе своих занятий и событий, не пропуская важные моменты!\n\n"
            'Для того, чтобы подключить расписание к календарю, нажмите на кнопку Добавить в календарь и следуйте инструкции.\n\n'
            "Спасибо, что вы с нами 🩷\n\n"
            "P.S. Также не забывайте подписываться на наш новостной канал @hse\\_perm\\_helper\\_news, иногда мы там выкладываем интересные штуки")

    keyboard_markup_up = ReplyKeyboardBuilder()
    get_schedule_text_button = types.KeyboardButton(text="💼 Расписание на неделю")
    get_base_schedule_text_button = types.KeyboardButton(text="🗓 Расписание на модуль")

    keyboard_markup_up.row(get_schedule_text_button)
    keyboard_markup_up.row(types.KeyboardButton(text="📅 На сегодня"), types.KeyboardButton(text="➡️ На завтра"))
    keyboard_markup_up.row(get_base_schedule_text_button, types.KeyboardButton(text="🏓 Расписание физ-ры"))
    keyboard_markup_up.row(types.KeyboardButton(text="🖥️ Добавить в календарь"), types.KeyboardButton(text="⚙️ Настройки"))
    keyboard_markup_up.row(types.KeyboardButton(text="⚡️ Быстрый VPN от Вышкинцев"), types.KeyboardButton(text="💳 Поддержать разработчиков"))
    keyboard_markup_up.row_width = 4

    keyboard = keyboard_markup_up.as_markup()
    keyboard.resize_keyboard = True

    await message.bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)


@required_admin
@router.message(Command("update"))
async def update(message: types.Message):
    text = ("* Наконец мы доделали это * 🎉\n\n"
            "Теперь вы можете легко добавить ваше расписание в календарь на мобильном устройстве 📱 или ПК 💻"
            "Это значит, что вы сможете всегда быть в курсе своих занятий и событий, не пропуская важные моменты!\n\n"
            'Для того, чтобы подключить расписание к календарю, нажмите на кнопку Добавить в календарь и следуйте инструкции.\n\n'
            "Спасибо, что вы с нами 🩷\n\n"
            "P.S. Также не забывайте подписываться на наш новостной канал @hse\\_perm\\_helper\\_news, иногда мы там выкладываем интересные штуки")

    keyboard_markup_up = ReplyKeyboardBuilder()
    get_schedule_text_button = types.KeyboardButton(text="💼 Расписание на неделю")
    get_base_schedule_text_button = types.KeyboardButton(text="🗓 Расписание на модуль")

    keyboard_markup_up.row(get_schedule_text_button)
    keyboard_markup_up.row(types.KeyboardButton(text="📅 На сегодня"), types.KeyboardButton(text="➡️ На завтра"))
    keyboard_markup_up.row(get_base_schedule_text_button, types.KeyboardButton(text="🏓 Расписание физ-ры"))
    keyboard_markup_up.row(types.KeyboardButton(text="🖥️ Добавить в календарь"), types.KeyboardButton(text="⚙️ Настройки"))
    keyboard_markup_up.row(types.KeyboardButton(text="⚡️ Быстрый VPN от Вышкинцев"), types.KeyboardButton(text="💳 Поддержать разработчиков"))
    keyboard_markup_up.row_width = 4

    keyboard = keyboard_markup_up.as_markup()
    keyboard.resize_keyboard = True

    ids = await user_service.get_user_ids()

    for user in ids:
        try:
            await message.bot.send_message(chat_id=user, text=text, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
        except:
            continue

    await message.answer("completed")
