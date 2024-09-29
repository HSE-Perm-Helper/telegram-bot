from aiogram import Router, F
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.types import Message

from data.data_service import data_service
from decorator.decorators import exception_handler, required_admin

router = Router()

@router.message(Command("update_sport_schedule"))
@required_admin
async def get_sport_schedule(message: Message):
    file_id = message.photo[0].file_id
    await data_service.set_data("SPORT_SCHEDULE_FILE_ID", file_id)
    await message.delete()
    await message.answer("Фотография расписания успешно обновлена!")


@router.message(Command("delete_sport_schedule"))
@required_admin
async def get_sport_schedule(message: Message):
    await data_service.set_data("SPORT_SCHEDULE_FILE_ID", "")
    await message.delete()
    await message.answer("Фотография расписания успешно удалена!")




@exception_handler
@router.message(F.text == "🏓 Расписание физ-ры")
async def get_today_lessons(message: Message):
    file_id = await data_service.get_data("SPORT_SCHEDULE_FILE_ID")
    await message.delete()
    await message.bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
    if len(file_id) == 0:
        await message.answer("Пока расписания физ-ры нет 😕")
        return

    await message.answer_photo(photo=file_id, caption="Расписание физ-ры на этот учебный год 💪")