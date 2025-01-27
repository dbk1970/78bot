import asyncio
import logging


from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot_files import config
from bot_files.handlers import router, logger


async def main():
    bot = Bot(token=config.AUTH_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    # logger = logging.getLogger(__name__)
    # file_handler = logging.FileHandler("data.log")
    logger.setLevel(logging.INFO)
    console = logging.StreamHandler()
    logging.basicConfig(level=logging.INFO, datefmt="%y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s",
        handlers=[console])
    asyncio.run(main())