from aiogram.dispatcher.filters import Filter
from aiogram.types import ChatType, Message
from config import ADMIN_ID


class PrivateChatFilter(Filter):
    async def check(self, message: Message) -> bool:
        return message.chat.type == ChatType.PRIVATE


class GroupChatFilter(Filter):
    async def check(self, message: Message) -> bool:
        chat_type = message.chat.type
        return chat_type in [ChatType.GROUP, ChatType.SUPER_GROUP]


class AdminFilter(Filter):
    async def check(self, message: Message) -> bool:
        user_id = message.from_user.id
        return user_id == ADMIN_ID


class NotAdminFilter(Filter):
    async def check(self, message: Message) -> bool:
        user_id = message.from_user.id
        return user_id != ADMIN_ID


class VerifyUsers(Filter):
    async def check(self, message: Message) -> bool:
        return message.from_user.username in ("cghael", "Anry_404", "Dhkdel", "Dudashvili_Vladislav")


class UnverifyUsers(Filter):
    async def check(self, message: Message) -> bool:
        return message.from_user.username not in ("cghael", "Anry_404", "Dhkdel", "Dudashvili_Vladislav")
