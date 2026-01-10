import asyncio
import logging

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from tortoise import Tortoise

from config.config import Config, load_config
from handlers import events, other, start
from http_client import close_session

logger = logging.getLogger(__name__)

async def set_main_menu(bot: Bot):
    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/help',
                description='Справка по работе бота'),
        BotCommand(command='/profile',
                description='Профиль пользователя'),
        BotCommand(command='/timetable',
                description='Узнать расписание'),
        BotCommand(command='/changedata',
                description='Изменить данные')
    ]
    await bot.set_my_commands(main_menu_commands)

async def main():
    config: Config = load_config()
    await Tortoise.init(db_url="sqlite://db.sqlite3",modules={"app":["db.models"]})
    await Tortoise.generate_schemas()
    logging.basicConfig(
        level=logging.getLevelName(level=config.log.level),
        format=config.log.format,
    )
    logger.info("Starting bot")

    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(start.router)
    dp.include_router(events.router)
    dp.include_router(other.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await set_main_menu(bot)
    try:
        await dp.start_polling(bot)
    finally:
        await close_session()

asyncio.run(main())
