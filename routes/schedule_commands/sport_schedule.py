from aiogram import Router, F
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, BufferedInputFile, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.data_service import data_service, DataField
from decorator.decorators import required_admin

router = Router()

@router.message(Command("update_sport_schedule"), F.photo)
@required_admin
async def update_sport_schedule(message: Message, state: FSMContext):
    await state.clear()

    photo_id = message.photo[0].file_id

    await data_service.set_data(DataField.SPORT_SCHEDULE_PHOTO_FILE_ID.value, photo_id)

    await message.delete()
    await message.answer("Фотография расписания успешно обновлена!")


@router.message(Command("delete_sport_schedule"))
@required_admin
async def get_sport_schedule(message: Message, state: FSMContext):
    await state.clear()

    await data_service.clear_data(DataField.SPORT_SCHEDULE_PHOTO_FILE_ID.value)
    await message.delete()
    await message.answer("Фотография расписания успешно удалена!")


@router.message(F.text == "🏓 Расписание физ-ры")
@router.message(Command("sport_schedule"))
async def get_today_lessons(message: Message, state: FSMContext):
    await state.clear()

    file_id = await data_service.get_data(DataField.SPORT_SCHEDULE_PHOTO_FILE_ID.value)
    await message.delete()

    if len(file_id) == 0:
        await message.answer("Пока расписания физ-ры нет 😕")
        return

    await state.clear()

    await message.bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
    await message.answer_photo(photo=file_id, caption="**Расписание физ-ры 💪**", show_caption_above_media=True)
