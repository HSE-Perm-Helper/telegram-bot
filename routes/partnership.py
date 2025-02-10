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
                                      url="https://t.me/sigmavpn_xbot?start=cHJvbW89SFNFX1BFUk1fSEVMUEVSJnNvdXJjZT1IU0VfSEVMUEVS"))

    await message.answer(
        "<b>Sigma VPN</b> – быстрый, недорогой и стабильный VPN на базе телеграмм бота с использованием протокола VLESS, созданный разработчиками этого бота ✨🧑‍💻\n\n" +
        "В сервисе нет ограничений по скорости, можно подключить хоть сколько устройств и наслаждаться комфортом со стабильным подключением 🔒",
        parse_mode=ParseMode.HTML, reply_markup=keyboard.as_markup())
