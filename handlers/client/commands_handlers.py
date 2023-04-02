from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from filters.chat_type import PrivateChatFilter, AdminFilter, VerifyUsers, UnverifyUsers

from keybords.client_kbrd import get_main_keyboard
from keybords.admin_kbrd import get_admin_keyboard

from config import ADMIN_ID
from handlers.client.utils import read_from_file_db, get_author_name


async def report(message: types.Message):
    user_data = read_from_file_db("summary")[message.from_user.username]
    take_text = ""
    give_text = ""
    for k, v in user_data.items():
        name = get_author_name(k)
        if v > 0:
            give_text += f"{name}: <b>{v}</b> лари\n"
        else:
            take_text += f"{name}: <b>{-v}</b> лари\n"

    await message.answer(
        f"<u>📉 Вы должны:</u>\n" + take_text + f"\n<u>📈 Вам должны:</u>\n" + give_text,
        parse_mode=types.ParseMode.HTML
    )


async def start_command(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = get_main_keyboard()
    await message.answer("Выбери команду, кожаный ублюдок!", reply_markup=keyboard)


async def start_command_others(message: types.Message):
    await message.answer("Ну и чо тебе надо, кожаный ублюдок?\n"
                         "Я работаю только для определенного круга пользователей.\n"
                         "Если интересно, напиши @cghael")


async def admin_command(message: types.Message, state: FSMContext):
    await state.finish()
    # TODO maybe some other admin check
    if ADMIN_ID != message.from_user.id:
        await message.answer("Простите, но хозяин запретил мне разговаривать об этом.")
        return
    keyboard = get_admin_keyboard()
    await message.answer("Выберите команду, хозяин!", reply_markup=keyboard)


def register_commands_handlers(dp: Dispatcher):
    dp.register_message_handler(
        start_command_others,
        UnverifyUsers(),
        PrivateChatFilter(),
        commands=['start']
    )
    dp.register_message_handler(
        start_command,
        PrivateChatFilter(),
        VerifyUsers(),
        commands=['start'],
        state="*"
    )
    dp.register_message_handler(
        admin_command,
        AdminFilter(),
        commands=['admin'],
        state="*"
    )
    dp.register_message_handler(
        report,
        PrivateChatFilter(),
        VerifyUsers(),
        content_types=['text'],
        text='📊 Отчет'
    )
