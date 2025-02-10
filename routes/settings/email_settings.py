import enum

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from api import user_service, verification_service
from decorator.decorators import typing_action
from exception.verification.cannot_resent_email_by_attempts_exception import CanNotResentEmailByAttemptsException
from exception.verification.cannot_resent_email_by_delay_exception import CannotResentEmailByDelayException
from exception.verification.invalid_email_format_exception import InvalidEmailFormatException
from exception.verification.user_already_exists_with_this_email_exception import UserAlreadyExistsWithThisEmailException
from exception.verification.verification_request_not_found_exception import VerificationRequestNotFoundException
from routes.settings import shared
from routes.settings.shared import SettingsCallback
from util.utils import number_format

router = Router()

class EmailSettingsCallback(enum.Enum):
    SET_EMAIL = "SET_EMAIL"
    RESENT_VERIFICATION = "RESENT_VERIFICATION"
    DELETE_EMAIL = "DELETE_EMAIL"
    BACK_TO_SETTINGS = "BACK"
    DONE = "DONE"
    CANCEL = "CANCEL"

class EmailSettingsState(StatesGroup):
    EMAIL_INFO = State()
    EMAIL_EDIT = State()


@router.callback_query(F.data == SettingsCallback.EMAIL_SETTINGS.value)
@typing_action
async def email_settings(query: CallbackQuery, state: FSMContext):
    await query.answer()

    user = await user_service.get_user(query.from_user.id)
    email: str | None = user["email"]

    await state.set_state(EmailSettingsState.EMAIL_INFO)

    if isinstance(email, str):
        return await email_settings_when_email_exists(email, query, state)

    return await email_settings_when_email_not_set(query, state)


async def email_settings_when_email_exists(email: str, query: CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="✏️ Изменить", callback_data=EmailSettingsCallback.SET_EMAIL.value)
    keyboard.button(text="❌ Удалить", callback_data=EmailSettingsCallback.DELETE_EMAIL.value)
    keyboard.button(text="⬅️ В настройки", callback_data=EmailSettingsCallback.BACK_TO_SETTINGS.value)
    keyboard.adjust(2, repeat=True)

    text = (f"📧 *Корпоративная почта: {email}*\n\
\n\
🔹 Привязка корпоративной почты позволяет боту выдавать более точное расписание\n\
🔹 В случае проблем с Telegram, некоторые уведомления будут приходить на почту")
    await query.message.edit_text(text, parse_mode=ParseMode.MARKDOWN)
    await query.message.edit_reply_markup(reply_markup=keyboard.as_markup())


async def email_settings_when_email_not_set(query: CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🔑 Привязать", callback_data=EmailSettingsCallback.SET_EMAIL.value)
    keyboard.button(text="⬅️ В настройки", callback_data=EmailSettingsCallback.BACK_TO_SETTINGS.value)
    keyboard.adjust(1)

    text = ("📧 *Корпоративная почта не привязана*\n\
\n\
🔹 Привязка корпоративной почты позволит боту выдавать более точное расписание\n\
🔹 В случае проблем с Telegram, некоторые уведомления могут приходить на почту")
    await query.message.edit_text(text, parse_mode=ParseMode.MARKDOWN)
    await query.message.edit_reply_markup(reply_markup=keyboard.as_markup())


@router.callback_query(F.data == EmailSettingsCallback.BACK_TO_SETTINGS.value)
async def back_to_settings(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await shared.back_to_settings(query, state)


@router.callback_query(F.data == EmailSettingsCallback.DONE.value)
async def done_settings(query: CallbackQuery, state: FSMContext):
    await query.answer("✅ Привязка почты завершена")
    await state.clear()
    await query.message.delete()


@router.callback_query(F.data == EmailSettingsCallback.CANCEL.value)
async def cancel_settings(query: CallbackQuery, state: FSMContext):
    await query.answer("✅ Привязка почты отменена")
    await state.clear()
    await query.message.delete()


@router.callback_query(F.data == EmailSettingsCallback.SET_EMAIL.value)
async def email_set_or_update(query: CallbackQuery, state: FSMContext):
    await query.answer()

    text = ("*Введите почту для привязки:*\n\n"
            "💡 Используйте только вашу личную корпоративную почту (например, name@edu.hse.ru)")
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="❌ Отмена", callback_data=EmailSettingsCallback.CANCEL.value)

    await query.message.edit_text(text, parse_mode=ParseMode.MARKDOWN)
    await query.message.edit_reply_markup(reply_markup=keyboard.as_markup())
    await state.set_state(EmailSettingsState.EMAIL_EDIT)


@router.message(EmailSettingsState.EMAIL_EDIT)
async def email_set_or_update_attempt(message: Message, state: FSMContext):
    await message.delete()

    try:
        verification_info = await user_service.set_or_update_user_email(message.from_user.id, message.text)

        text = (f"✅ *Письмо с подтверждением было выслано на почту {message.text}* \n\n"
                "Нажмите на ссылку в письме, чтобы подтвердить свой email")

        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="🔄 Отправить заново",
                        callback_data=f"{EmailSettingsCallback.RESENT_VERIFICATION.value}{verification_info.token}")
        keyboard.row(InlineKeyboardButton(text="✅ Готово", callback_data=EmailSettingsCallback.DONE.value),
                     InlineKeyboardButton(text="❌ Отмена", callback_data=EmailSettingsCallback.CANCEL.value))

        await message.answer(text, reply_markup=keyboard.as_markup(), parse_mode=ParseMode.MARKDOWN)
        await state.clear()

    except InvalidEmailFormatException:
        text = ("*Неверный формат почты 😔*\n\n"
                "💡 Используйте только вашу личную корпоративную почту (например, name@edu.hse.ru)")

        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="❌ Отмена", callback_data=EmailSettingsCallback.CANCEL.value)

        await message.answer(text, reply_markup=keyboard.as_markup(), parse_mode=ParseMode.MARKDOWN)

    except UserAlreadyExistsWithThisEmailException:
        text = ("*Эта почта уже привязана к другому пользователю 😔*\n\n"
                "💡 Используйте только вашу личную корпоративную почту (например, name@edu.hse.ru)")

        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="❌ Отмена", callback_data=EmailSettingsCallback.CANCEL.value)

        await message.answer(text, reply_markup=keyboard.as_markup(), parse_mode=ParseMode.MARKDOWN)


@router.callback_query(F.data.startswith(EmailSettingsCallback.RESENT_VERIFICATION.value))
async def email_resent(query: CallbackQuery, state: FSMContext):
    token = query.data.replace(EmailSettingsCallback.RESENT_VERIFICATION.value, "")

    try:
        await verification_service.resend_verification(token)
        await query.answer("✅ Письмо успешно переотправлено")
    except CannotResentEmailByDelayException as e:
        formatted_seconds = number_format(e.delay, "секунду", "секунды", "секунд")
        await query.answer(f"💡 Письмо можно переотправить через {formatted_seconds}")
    except CanNotResentEmailByAttemptsException as e:
        await query.answer("⚠️ Больше нельзя переотправлять письмо, начните подтверждение заново")
    except VerificationRequestNotFoundException:
        await query.answer("😔 Запрос на верификацию истек, начните процесс заново")
        await query.message.delete()

@router.callback_query(F.data == EmailSettingsCallback.DELETE_EMAIL.value)
async def email_delete(query: CallbackQuery, state: FSMContext):
    await user_service.delete_user_email(query.from_user.id)

    await query.answer("✅ Почта успешно отвязана")
    await email_settings_when_email_not_set(query, state)
