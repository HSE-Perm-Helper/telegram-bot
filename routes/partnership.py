from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()

@router.message(F.text == "⚡️ Быстрый VPN от Вышкинцев")
@router.message(Command("vpn"))
async def get_settings(message: Message, state: FSMContext):
    await state.clear()

    await message.delete()
    await message.answer("да-да он")