import asyncio
import logging
import os.path

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot_files.config import PATH_YAML
from bot_files.handlers import router, run_scheduler_to_start
from bot_files.logic import bot, groups
from bot_files.models import read_groups

logger = logging.getLogger(__name__)
if os.path.exists(PATH_YAML): read_groups()

async def main()->None:
    """ Собственно главная функция """
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    for i_d in groups.keys(): asyncio.create_task(run_scheduler_to_start(i_d))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    console = logging.StreamHandler()
    logging.basicConfig(level=logging.INFO, datefmt="%y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s",
        handlers=[console])
    asyncio.run(main())