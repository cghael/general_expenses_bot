from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types


allowed_names = ["Антон", "Андрей", "Андрбай", "Влади"]


def cancel_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = "❌ Отмена"
    keyboard.add(button)
    return keyboard


def names_keyboard(author_name):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    names_list = allowed_names.copy()
    names_list.remove(author_name)

    odd_button = None
    if len(names_list) % 2 == 0:
        button_list = [[names_list[i], names_list[i + 1]] for i in range(0, len(names_list), 2)]
    else:
        button_list = [[names_list[i], names_list[i + 1]] for i in range(0, len(names_list[:-1]), 2)]
        odd_button = names_list[-1]

    for buttons in button_list:
        keyboard.add(*buttons)
    keyboard.add(odd_button)
    keyboard.add(*["👨‍👨‍👦‍👦 На всех", "🗑️ Очистить"])
    keyboard.add(*["❌ Отмена", "⏭️ Далее"])
    return keyboard


def confirm_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = ["❌ Отмена", "✅ Подтвердить"]
    keyboard.add(*button)
    return keyboard


def get_main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["📊 Отчет", "💸 Записать траты"]
    keyboard.add(*buttons)
    return keyboard
