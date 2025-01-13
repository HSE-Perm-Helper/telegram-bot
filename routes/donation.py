from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message

router = Router()

@router.message(F.text == "💳 Поддержать разработчиков")
async def donation(message: Message):
    text = ("*Поддержите разработку нашего бота 😊*\n\n"
            "Мы создаём этот бот на чистом энтузиазме, и ваша поддержка очень важна для нас. "
            "Если вам нравится наш проект, будем благодарны за любую помощь ❤️\n\n"
            "*💳 Реквизиты (нажмите, чтобы скопировать):*\n"
            "СБП: `+79519574508` (Т-банк)")
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)