import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from tortoise import Tortoise

from config.config import Config, load_config
from handlers import events, other, start

logger = logging.getLogger(__name__)


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
    await dp.start_polling(bot)


asyncio.run(main())
