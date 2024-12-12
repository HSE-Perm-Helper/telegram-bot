from lib2to3.fixer_util import Comma

from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from api import user_service
from bot import bot
from decorator.decorators import required_admin

router = Router()


@router.message(F.text == "⚡️ Быстрый VPN от Вышкинцев")
@router.message(Command("vpn"))
async def get_settings(message: Message, state: FSMContext):
    await state.clear()
    await message.delete()

    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="⚡️Перейти в бота",
                                      url="https://t.me/sigmavpn_xbot?start=cHJvbW89SFNFX1BFUk1fSEVMUEVSJnNvdXJjZT1IU0VfSEVMUEVS"))

    await message.answer(
        "<b>Sigma VPN</b> – быстрый, недорогой и стабильный VPN на базе телеграмм бота с использованием протокола VLESS, созданный разработчиками этого бота ✨🧑‍💻\n\n" +
        "В сервисе нет ограничений по скорости, можно подключить хоть сколько устройств и наслаждаться комфортом со стабильным подключением 🔒",
        parse_mode=ParseMode.HTML, reply_markup=keyboard.as_markup())


@router.message(Command("test"))
async def test(message: Message):
    text = ("*Привет, студент!* 👋\n\n"
            "Разработчики нашего бота с расписанием создали новый продукт – *Sigma VPN!*\n"
            "Он быстрее и стабильнее, чем OKVPN, и... дешевле! 🚀\n\n"

            "Переходи в бот по ссылке и получи *3 дня бесплатного доступа!* 🤩\n\n"

            "Защити свои данные с Sigma VPN! 🔐")

    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="⚡️Перейти в бота",
                                      url="https://t.me/sigmavpn_xbot?start=cHJvbW89SFNFX1BFUk1fSEVMUEVSJnNvdXJjZT1IU0VfSEVMUEVS"))

    await message.answer(text, reply_markup=keyboard.as_markup(), parse_mode=ParseMode.MARKDOWN)


@router.message(Command("sigmavpn1"))
@required_admin
async def mailing_sigmavpn(message: Message):
    await __mailing(message, 1)

@router.message(Command("sigmavpn2"))
@required_admin
async def mailing_sigmavpn2(message: Message):
    await __mailing(message, 2)


@router.message(Command("sigmavpn3"))
@required_admin
async def mailing_sigmavpn3(message: Message):
    await __mailing(message, 3)


@router.message(Command("sigmavpn4"))
@required_admin
async def mailing_sigmavpn4(message: Message):
    await __mailing(message, 4)


@router.message(Command("sigmavpn5"))
@required_admin
async def mailing_sigmavpn5(message: Message):
    await __mailing(message, 0)


async def __mailing(message: Message, num: int):
    await message.delete()
    await message.answer("Рассылка началась")

    users = await user_service.get_user_ids()

    text = ("*Привет, студент!* 👋\n\n"
            "Разработчики нашего бота с расписанием создали новый продукт – *Sigma VPN!*\n"
            "Он быстрее и стабильнее, чем OKVPN, и... дешевле! 🚀\n\n"

            "Переходи в бот по ссылке и получи *3 дня бесплатного доступа!* 🤩\n\n"

            "Защити свои данные с Sigma VPN! 🔐")

    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="⚡️Перейти в бота",
                                      url="https://t.me/sigmavpn_xbot?start=cHJvbW89SFNFX1BFUk1fSEVMUEVSJnNvdXJjZT1IU0VfSEVMUEVS"))

    actual = 0

    expected = 0
    for i, user in enumerate(users):
        if i % 5 == num:
            expected += 1
            try:
                await bot.send_message(user, text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard.as_markup())
                actual += 1
            except Exception as e:
                pass

    await message.answer(f"Рассылка успешно отправлена! Всего попыток – {expected}, успешно – {actual}")
