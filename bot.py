import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.config_reader import load_config
from app.handlers.binary_to_text import register_binary_to_text
from app.handlers.common import register_handlers_common
from app.handlers.text_to_binary import register_text_to_binary

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    #
    config = load_config("config/bot.ini")
    #
    bot = Bot(token=config.bot.TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())
    #
    register_binary_to_text(dp)
    register_text_to_binary(dp)
    register_handlers_common(dp)
    #
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
