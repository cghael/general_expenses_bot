from aiogram import Dispatcher

from handlers import client
from handlers import admin
from handlers import other


def register_all_handlers(dispatcher: Dispatcher):
    handlers = (
        # admin.commands_handlers.register_admin_handlers,
        client.commands_handlers.register_commands_handlers,
        client.spend_money_handler.register_state_handlers,
        other.register_handlers_other
    )
    for register in handlers:
        register(dispatcher)
