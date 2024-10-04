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

DOCUMENT_TYPE_CALLBACK = "DOCUMENT"
PHOTO_TYPE_CALLBACK = "PHOTO"


class SportScheduleState(StatesGroup):
    WAITING_TYPE_OF_SEND = State()


@router.message(Command("update_sport_schedule"), F.photo)
@required_admin
async def get_sport_schedule(message: Message, state: FSMContext):
    await state.clear()

    photo_id = message.photo[0].file_id

    await data_service.set_data(DataField.SPORT_SCHEDULE_PHOTO_FILE_ID.value, photo_id)

    await message.delete()
    await message.answer("Фотография расписания успешно обновлена!")


@router.message(Command("update_sport_schedule"), F.document)
@required_admin
async def get_sport_schedule(message: Message, state: FSMContext):
    await state.clear()

    document_file_id = message.document.file_id
    file_path = await message.bot.get_file(document_file_id)
    file = await message.bot.download_file(file_path.file_path)
    file_extension = message.document.file_name.split(".")[-1]
    file_name = f"sport-schedule.{file_extension}"
    input_file = BufferedInputFile(file.read(), file_name)

    document_message = await message.answer_document(input_file)
    await document_message.delete()

    document_id = document_message.document.file_id

    await data_service.set_data(DataField.SPORT_SCHEDULE_DOCUMENT_FILE_ID.value, document_id)

    await message.delete()
    await message.answer("Документ расписания успешно обновлена!")


@router.message(Command("delete_sport_schedule"))
@required_admin
async def get_sport_schedule(message: Message, state: FSMContext):
    await state.clear()

    await data_service.clear_data(DataField.SPORT_SCHEDULE_DOCUMENT_FILE_ID.value)
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

    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="Документом 📄", callback_data=DOCUMENT_TYPE_CALLBACK))
    keyboard.row(InlineKeyboardButton(text="Фотографией 🖼️", callback_data=PHOTO_TYPE_CALLBACK))

    await message.answer("Выбери способ получения расписания:", reply_markup=keyboard.as_markup())
    await state.set_state(SportScheduleState.WAITING_TYPE_OF_SEND)


@router.callback_query(SportScheduleState.WAITING_TYPE_OF_SEND, F.data == DOCUMENT_TYPE_CALLBACK)
async def handle_document_type_schedule(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.delete()

    file_id = await data_service.get_data(DataField.SPORT_SCHEDULE_DOCUMENT_FILE_ID.value)

    await query.message.bot.send_chat_action(query.message.chat.id, ChatAction.UPLOAD_DOCUMENT)
    await query.message.answer_document(document=file_id, caption="Расписание физ-ры 💪")


@router.callback_query(SportScheduleState.WAITING_TYPE_OF_SEND, F.data == PHOTO_TYPE_CALLBACK)
async def handle_document_type_schedule(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.delete()

    file_id = await data_service.get_data(DataField.SPORT_SCHEDULE_PHOTO_FILE_ID.value)

    await query.message.bot.send_chat_action(query.message.chat.id, ChatAction.UPLOAD_PHOTO)
    await query.message.answer_photo(photo=file_id, caption="Расписание физ-ры 💪")
