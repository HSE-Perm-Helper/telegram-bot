import dataclasses
from asyncio import sleep

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.data_service import DataField, data_service
from decorator.decorators import typing_action, required_admin
from util.utils import parse_boolean

router = Router()

class AdminSettingsState(StatesGroup):
    OPENED_SETTINGS = State()

@dataclasses.dataclass()
class AdminSettings:
    name: str
    key: str


def _get_settings() -> list[AdminSettings]:
    return [
        AdminSettings("Проверка уведомлений", DataField.IS_ENABLED_NOTIFICATIONS_FETCH.value),
        AdminSettings("Проверка работы бэка", DataField.IS_ENABLED_BACKEND_HEALTH_CHECK.value)
    ]

@router.message(Command("bot_settings"))
@typing_action
@required_admin
async def bot_settings_command(message: Message, state: FSMContext):
    await state.clear()

    await message.delete()
    text = "⚙️ Настройки бота"
    keyboard = await __get_settings_keyboard()
    await message.answer(text, reply_markup=keyboard.as_markup())
    await state.set_state(AdminSettingsState.OPENED_SETTINGS)


async def __get_settings_keyboard():
    keyboard = InlineKeyboardBuilder()

    for setting in _get_settings():
        value = parse_boolean(await data_service.get_data(setting.key))
        keyboard.row(InlineKeyboardButton(text=f"{__get_state_for_setting(value)} {setting.name}", callback_data=setting.key))

    keyboard.row(InlineKeyboardButton(text="Готово", callback_data="done"))
    return keyboard


@router.callback_query(AdminSettingsState.OPENED_SETTINGS)
async def process_setting(query: CallbackQuery, state: FSMContext):
    await query.answer()
    if query.data == "done":
        await state.clear()
        await query.message.delete()
        return

    for setting in _get_settings():
        if setting.key == query.data:
            value = parse_boolean(await data_service.get_data(setting.key))
            new_value = not value
            await data_service.set_data(setting.key, new_value)
            keyboard = await __get_settings_keyboard()
            await query.message.edit_reply_markup(reply_markup=keyboard.as_markup())
            break


def __get_state_for_setting(value: bool) -> str:
    symbol = "✅"
    if not value:
        symbol = "❌"
    return symbol


@router.message(Command("sorry"))
async def sorry_notifications(message: Message):
    await message.answer("Прости за флуд от бота, он больше так не будет 😔")
    await message.bot.send_sticker(message.chat.id, sticker="CAACAgIAAxkBAAIQY2ct8ukfy3TW-l3RaEnueMQFwUwpAAK2EQAC0KdoS7opz7ewoj-9NgQ")


@router.message(Command("sorry_2"))
async def sorry_notifications2(message: Message):
    ids = {1620810043, 550344858, 391917168, 668836447, 886202688, 834260019, 407642716, 1314704840, 1021434584,
           1480455282, 1226199614, 855604608, 480867868,
           327010214,
           452362770,
           1266423210,
           748922869,
           735118961,
           358302372,
           408212381,
           733200318,
           1119876160,
           938373934,
           680161013,
           487908652,
           1358860192,
           991367605,
           1144786442,
           959453752,
           5395858524,
           1200117322,
           1308623688,
           803523914,
           974874777,
           1285528241,
           5743280577,
           1053013507,
           888346818,
           904316792,
           1100384168,
           934686546,
           994986445,
           1898172485,
           586129282,
           596396505,
           1176742239,
           224741598,
           1244785856,
           1067576781,
           1366540676,
           1659348641,
           844772001,
           970190451,
           731223283,
           1110724696,
           648755426,
           952290418,
           1047041954,
           1136581433,
           1073925130,
           1452995209,
           915964153,
           1608482152,
           511533992,
           5674830761,
           1410165613,
           831133881,
           885522311,
           482287073,
           872555833,
           2052461498,
           5228869950,
           579261947,
           1413309362,
           532097524,
           387399841,
           752982763,
           5009882212,
           1694698220,
           1245170512,
           1221231124,
           685273613,
           1175657393,
           5828611460
           }
    for user in ids:
        try:
            await message.bot.send_message(user, "Прости за флуд от бота, он больше так не будет 😔")
            await message.bot.send_sticker(user,
                                           sticker="CAACAgIAAxkBAAIQY2ct8ukfy3TW-l3RaEnueMQFwUwpAAK2EQAC0KdoS7opz7ewoj-9NgQ")
            await sleep(0.5)
        except Exception as e:
            continue
    await message.answer("готово))")

