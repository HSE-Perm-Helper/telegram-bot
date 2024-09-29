import asyncio

from aiogram import types

from bot import bot, dp
from data.data_service import DataService
from routes import mailing, menu, partnership
from routes.command_handle import commands
from routes.registration import registration
from routes.schedule_handle import schedule_handle, today_schedule, tomorrow_schedule, sport_schedule
from worker import workers

async def main():
    workers.run_workers()
    dp.include_router(commands.router)
    dp.include_router(registration.router)
    dp.include_router(schedule_handle.router)
    dp.include_router(today_schedule.router)
    dp.include_router(tomorrow_schedule.router)
    dp.include_router(sport_schedule.router)
    dp.include_router(partnership.router)
    dp.include_router(mailing.router)
    dp.include_router(menu.router)


    # Команды бота в списке

    await bot.set_my_commands([
        types.BotCommand(command='help', description='Помощь с работой бота'),
        types.BotCommand(command='settings', description='Изменить данные о себе'),
        types.BotCommand(command='menu', description='Вызвать меню'),
        types.BotCommand(command='schedule', description='Получить расписание'),
        types.BotCommand(command='base_schedule', description='Получить расписание на модуль'),
    ], scope=types.BotCommandScopeDefault())

    await dp.start_polling(bot)


# Запуск запланированных задач в отдельном потоке
if __name__ == "__main__":
    asyncio.run(main())
