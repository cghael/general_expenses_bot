from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types


def get_admin_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["✏️ записать пользователей", ]
    keyboard.add(*buttons)
    return keyboard
