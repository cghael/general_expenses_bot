from aiogram.utils import executor
from loguru import logger

from create_bot import dp
from handlers.main import register_all_handlers


async def on_startup(_):
    logger.info('Bot starts')
    register_all_handlers(dp)
    print("Bot starts working...")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
