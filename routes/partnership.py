from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "⚡️ Быстрый VPN от Вышкинцев")
async def get_settings(message: Message):
    await message.delete()
    await message.answer("да-да он")