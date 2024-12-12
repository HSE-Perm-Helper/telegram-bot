from dotenv import load_dotenv

load_dotenv()

import asyncio

from aiogram import types

from bot import bot, dp
from middleware.exception_handler_middleware import ExceptionHandlerMiddleware
from routes import mailing, menu, partnership, settings_command, registration, start, admin_settings
from routes.schedule_commands import schedule_handle, today_schedule, tomorrow_schedule, sport_schedule
from worker import workers


async def main():
    workers.run_workers()

    dp.update.middleware.register(ExceptionHandlerMiddleware())

    dp.include_router(start.router)
    dp.include_router(schedule_handle.router)
    dp.include_router(registration.router)
    dp.include_router(settings_command.router)
    dp.include_router(today_schedule.router)
    dp.include_router(tomorrow_schedule.router)
    dp.include_router(sport_schedule.router)
    dp.include_router(partnership.router)
    dp.include_router(mailing.router)
    dp.include_router(menu.router)
    dp.include_router(admin_settings.router)

    # Команды бота в списке

    await bot.set_my_commands([
        types.BotCommand(command='help', description='Помощь с работой бота'),
        types.BotCommand(command='settings', description='Настройки'),
        types.BotCommand(command='menu', description='Вызвать меню'),
        types.BotCommand(command='schedule', description='Получить расписание'),
        types.BotCommand(command='base_schedule', description='Получить расписание на модуль'),
        types.BotCommand(command='sport_schedule', description="Получить расписание физ-ры"),
        types.BotCommand(command='today', description="Получить расписание на сегодня"),
        types.BotCommand(command='tomorrow', description="Получить расписание на завтра"),
        types.BotCommand(command='vpn', description="VPN от создателей бота")
    ], scope=types.BotCommandScopeDefault())

    await dp.start_polling(bot)


# Запуск запланированных задач в отдельном потоке
if __name__ == "__main__":
    asyncio.run(main())
