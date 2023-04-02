import yaml
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from create_bot import bot
from filters import PrivateChatFilter, GroupChatFilter, AdminFilter
from keybords.client_kbrd import get_main_keyboard, cancel_keyboard, confirm_keyboard
from keybords.admin_kbrd import get_admin_keyboard


async def read_users(message: types.Message):
    chat = await bot.get_chat(message.chat.id)
    members_list = {}
    for member in chat.members:
        user_id = member.user.id
        username = member.user.username
        members_list[username] = user_id
    file_path = f"file_database/users_from_chat.yaml"
    with open(file_path, "w") as f:
        yaml.dump(members_list, f)
    await message.answer("👮‍♂️Все записано!")


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(
        read_users,
        AdminFilter(),
        GroupChatFilter(),
        content_types=['text'],
        text='✏️ записать пользователей'
    )
