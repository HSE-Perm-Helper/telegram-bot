from aiogram import types

from callback.callback import insert_data_to_callback
from callback.schedule_callback import ScheduleCallback
from constants import constant
from schedule.schedule_type import ScheduleType

emojies_for_week_color = ['🟥', '🟪', '🟦', '🟩', '🟧', '🟨']


def get_button_text_by_schedule_info(schedule_info: dict, start: str, end: str) -> str:
    schedule_type = schedule_info["scheduleType"]
    match schedule_type:
        case ScheduleType.COMMON_SCHEDULE.value:
            number = schedule_info["number"]
            return f"Неделя {number}, {start} — {end}"
        case ScheduleType.SESSION_SCHEDULE.value:
            return f"Сессия, {start} — {end}"
        case ScheduleType.QUARTER_SCHEDULE.value:
            number = schedule_info["number"]
            return f"Базовое расписание на {number} модуль"
    return "N/a"


def get_schedule_header_by_schedule_info(schedule_info: dict) -> str:
    schedule_type = schedule_info["scheduleType"]
    match schedule_type:
        case ScheduleType.COMMON_SCHEDULE.value:
            number = schedule_info["number"]
            emoji_index = number % len(emojies_for_week_color)
            emoji = emojies_for_week_color[emoji_index]
            return f"{emoji} Расписание на {number} неделю {emoji}"
        case ScheduleType.SESSION_SCHEDULE.value:
            return f"🍀 Расписание на сессию 🍀"
        case ScheduleType.QUARTER_SCHEDULE.value:
            number = schedule_info["number"]
            return f"🗓 Расписание на {number} модуль 🗓"
    return "N/a"


def get_button_by_schedule_info(schedule_info: dict, need_delete_message: bool) -> types.InlineKeyboardButton:
    data, end, start = get_callback_for_schedule(need_delete_message, schedule_info)
    return types.InlineKeyboardButton(text=get_button_text_by_schedule_info(schedule_info, start, end),
                                      callback_data=data)


def get_callback_for_schedule(need_delete_message, schedule_info):
    start = schedule_info["start"]
    end = schedule_info["end"]
    data = insert_data_to_callback(ScheduleCallback.TEXT_SCHEDULE_CHOICE.value, [start, end, need_delete_message])
    return data, end, start


def group_lessons_by_key(lessons: list[dict], key_func) -> dict[str, list[dict]]:
    lessons_by_key = {}
    for lesson in lessons:
        key = key_func(lesson)
        if key not in lessons_by_key:
            lessons_by_key[key] = []
        lessons_by_key[key].append(lesson)
    return lessons_by_key


def get_lesson_as_string(lesson):
    text_for_message = ''

    '''ОТНОСИТСЯ К КОСТЫЛЮ С ПОДГРУППАМИ'''
    subgroup = ""

    '''Если вид пары — майнор'''
    if lesson['lessonType'] == 'COMMON_MINOR':
        text_for_message = f"{constant.type_of_lessons_dict[lesson['lessonType']]}\n"

    else:
        '''Вычисляем время пары'''
        time_of_pair = f"{lesson['time']['startTime']} — {lesson['time']['endTime']}"

        if lesson['time']['startTime'] is not None and lesson['time']['endTime'] != None:
            '''Добавляем в сообщение номер пары'''
            text_for_message += f"<b>{constant.number_of_pair_dict[lesson['time']['startTime']]} </b>"

            '''Добавляем в сообщение время пары и ее тип'''
            text_for_message += (f"{time_of_pair} "
                                 f"{constant.type_of_lessons_dict[lesson['lessonType']]}\n")

            '''Добавляем в сообщение название пары'''

            # if lesson['lessonType'] in constant.type_of_lessons_dict.keys():
            #     text_for_message += (f"{lesson['subject']}\n")

            '''ТУТ ПОКА ЧТО КОСТЫЛЬ, В СЛУЧАЕ ИЗМЕНЕНИЯ НАЗВАНИЯ ПАР НА БЭКЕ СНЕСТИ ЭТОТ КУСОК И
            И РАСКОМЕНТИРОВАТЬ ВЕРХНИЙ, НО СНИЗУ НАДО БУДЕТ ЕЩЕ ДОПИСАТЬ КОД'''

            if lesson['lessonType'] in constant.type_of_lessons_dict.keys():
                if "подгруппа" in lesson['subject']:
                    pair_name_with_subgroup: str = lesson['subject']
                    pair_name = pair_name_with_subgroup[:len(pair_name_with_subgroup) - 21]
                    ' <b>(8 подгруппа)</b>'
                    subgroup = pair_name_with_subgroup[len(pair_name) + 5]
                    text_for_message += pair_name + "\n"
                else:
                    if lesson['lessonType'] in constant.type_of_lessons_dict.keys():
                        text_for_message += (f"{lesson['subject']}\n")

            '''КОНЕЦ КОСТЫЛЯ'''

        if lesson['lecturer'] is not None:
            '''Добавляем преподавателя пары'''
            text_for_message += (f"<i>{lesson['lecturer']} </i>")

        '''Проверяем, дистант или очная'''
        if lesson['isOnline']:

            '''- Если дистант, добавляем ссылки'''

            '''ТОТ САМЫЙ КОСТЫЛЬ ВНИЗУ'''
            if subgroup != "":
                text_for_message += f", {subgroup} п.г."
            else:
                text_for_message += "\n"
            '''КОНЕЦ КОСТЫЛЯ'''

            if lesson['links'] is None:
                text_for_message += (f"\nДистанционная пара, ссылки отсутствуют\n")

            else:
                text_for_message += (f"\nДистанционная пара, ссылки:\n")
                for link in lesson['links']:
                    text_for_message += (f"{link}\n")

        else:
            '''...иначе добавляем корпус и кабинет'''
            if lesson['places'] is not None:
                if len(lesson['places']) == 1:
                    place = lesson['places'][0]
                    text_for_message += (
                        f"{place['office']} [{place['building']}]")

                    '''ТОТ САМЫЙ КОСТЫЛЬ ВНИЗУ'''
                    if subgroup != "":
                        text_for_message += f", {subgroup} п.г.\n"
                    else:
                        text_for_message += "\n"
                    '''КОНЕЦ КОСТЫЛЯ'''

                else:
                    text_for_message += f'несколько мест:\n'
                    for place in lesson['places']:
                        '''- Иначе добавляем номер корпуса и аудиторию'''
                        text_for_message += (
                            f"{place['office']} [{place['building']}]")

                        '''ТОТ САМЫЙ КОСТЫЛЬ ВНИЗУ'''
                        if subgroup != "":
                            text_for_message += f", {subgroup} п.г.\n"
                        else:
                            text_for_message += "\n"
                        '''КОНЕЦ КОСТЫЛЯ'''

        '''Проверяем наличие дополнительной информации к паре'''
        if lesson['additionalInfo'] is not None:
            for addInfo in lesson['additionalInfo']:
                text_for_message += (f"\n<i>Доп.информация: — {addInfo}</i> \n")

        text_for_message += "\n"
    return text_for_message


async def get_pair_count(lesson_list):
    count_pairs = 0
    for pair in lesson_list:
        if pair:
            count_pairs += 1
    return count_pairs


async def group_lessons_by_pair_number(lessons):
    last_pair = constant.number_of_pair_dict[lessons[- 1]["time"]['startTime']]
    # lessons_list_count = int(last_pair.replace('-ая пара', ''))
    lessons_list_count = constant.emoji_to_int_dict[last_pair]
    lesson_list: list[None | list[dict]] = [None] * lessons_list_count
    ''' Тут я делаю проход по парам за день, в нем расставляю в массиве пары
                Потом иду по этому массиву и проверяю, 0 там или словарь. Если словарь - раскрываю его
                Иначе вывожу сообщение "Окно" '''
    for lesson in lessons:
        pair_index_string = constant.number_of_pair_dict[lesson["time"]["startTime"]]
        # pair_index = int(pair_index_string.replace('-ая пара', '')) - 1
        pair_index = constant.emoji_to_int_dict[pair_index_string] - 1

        if lesson_list[pair_index] is None:
            lesson_list[pair_index] = []

        lesson_list[pair_index].append(lesson)
    return lesson_list


async def get_lessons_without_header(lesson_list):
    text_for_message = ""
    is_pairs_start = False
    number_of_pair = 0
    for lessons_inner in lesson_list:
        if not is_pairs_start:
            if lessons_inner:
                is_pairs_start = True
        if not lessons_inner:
            if is_pairs_start:
                # text_for_message += f"<b>{number_of_pair + 1}-ая пара</b>"
                text_for_message += constant.int_to_emoji_dict[number_of_pair + 1]
                text_for_message += f" - ОКНО 🪟\n\n"

        else:
            for lesson in lessons_inner:
                text_for_message += get_lesson_as_string(lesson)
        number_of_pair += 1
    return text_for_message


async def get_lesson_message_header(count_pairs, day, is_session):
    if is_session:
        return f"<b>{day}</b>\n\n"
    else:
        return (f"<b>{day} — "
                f"{constant.count_pairs_dict[count_pairs]}</b>\n\n")
