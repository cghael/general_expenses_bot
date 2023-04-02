import re

from aiogram import types, Dispatcher
from loguru import logger
from filters.chat_type import GroupChatFilter, AdminFilter, NotAdminFilter
from handlers.client.utils import write_to_file_db


async def xru_xru(message: types.Message):
    logger.info(message)  # TODO del
    if re.findall(r"[Пп]одсвин\w+", message.text):
        await message.reply(text="хрю-хрю")


async def save_chat_id(message: types.Message):
    data = {"chat_message": message.chat}
    write_to_file_db("info", data)
    await message.reply("Все данные сохранены 📝")


async def save_chat_id_not_admin(message: types.Message):
    await message.reply("Ацтань!")


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(
        save_chat_id,
        GroupChatFilter(),
        AdminFilter(),
        content_types=['text'],
        text='Сохрани данные'
    )
    dp.register_message_handler(
        save_chat_id_not_admin,
        NotAdminFilter(),
        content_types=['text'],
        text='Сохрани данные'
    )
    dp.register_message_handler(
        xru_xru,
        GroupChatFilter()
    )
