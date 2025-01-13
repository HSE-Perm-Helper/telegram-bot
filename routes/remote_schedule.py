from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from api.user_service import get_remote_schedule_link

router = Router()

@router.message(F.text == "🖥️ Добавить в календарь")
async def remote_schedule(message: Message):
    model = await get_remote_schedule_link(message.from_user.id)
    base_link = model.link

    text = (f"Вы можете добавить *обновляемое* расписание в свой календарь в Google, Календарь iOS и другие приложения календарей, "
            f"если они поддерживают получение календаря по URL в формате iCal.\n\n"
            "🔗 Для этого скопируйте эту ссылку:\n\n"
            f"`{base_link}`\n\n"
            "❗Не скачивайте этот файл и не открывайте ссылку в браузере, иначе вы получите необновляемое расписание.\n\n"
            "*Для автоматического подключения воспользуйтесь одной из кнопок внизу сообщения 👇* \n\nЕсли вы не нашли там свой календарь, "
            "следуйте этой инструкции:\n\n"
            "*Яндекс Календарь*\n\n"
            "Перейдите по этой [ссылке](https://calendar.yandex.ru/week?sidebar=addFeed) и вставьте скопированный адрес. Задайте имя, выберите цвет "
            "и нажмите «Создать».")

    base_link = base_link.replace("https://", "")
    direct_link = "https://api.hse-perm-helper.ru/remote-schedule/redirect?target=webcal://" + base_link

    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="📕 Apple Calendar", url=direct_link)
    keyboard.button(text="📗 Google Calendar", url=f"https://calendar.google.com/calendar/r?cid=webcal://{base_link}")
    keyboard.button(text="📘 Outlook", url=direct_link)
    keyboard.button(text="📙 Microsoft 365", url=f"https://outlook.office.com/calendar/0/addfromweb?url=webcal://{base_link}")

    keyboard.adjust(1)

    await message.answer(text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True, reply_markup=keyboard.as_markup())
