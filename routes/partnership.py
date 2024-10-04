from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.message(F.text == "⚡️ Быстрый VPN от Вышкинцев")
@router.message(Command("vpn"))
async def get_settings(message: Message, state: FSMContext):
    await state.clear()
    await message.delete()

    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="⚡️Перейти в бота",
                                      url="https://t.me/okvpn_xbot?start=ref__ec6e9bd3-54b2-4ee3-9965-6263c4fd981b"))

    await message.answer(
        "<b>OKVPN</b> – быстрый и недорогой VPN на базе телеграмм бота, созданный студентами Вышки ✨🧑‍💻\n\n" +
        "В сервисе нет ограничений по скорости, можно подключить хоть сколько устройств и людей и выбрать любую из 11 стран🌎",
        parse_mode=ParseMode.HTML, reply_markup=keyboard.as_markup())
