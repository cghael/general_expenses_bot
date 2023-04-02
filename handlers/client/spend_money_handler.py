from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from utilities.states import SpendMoney
from keybords.client_kbrd import get_main_keyboard, cancel_keyboard, names_keyboard, confirm_keyboard
from handlers.client.utils import get_author_name
from filters.chat_type import PrivateChatFilter
from handlers.client.utils import save_transaction_to_db, save_history_db
from create_bot import bot


allowed_names = ["Антон", "Андрей", "Андрбай", "Влади"]


async def cancel_handler(message: types.Message, state: FSMContext):
    await message.answer("Ввод прекращен", reply_markup=get_main_keyboard())
    await state.finish()


async def spend_money(message: types.Message, state: FSMContext):
    keyboard = cancel_keyboard()
    await message.answer("Введите потраченную сумму:", reply_markup=keyboard)
    await state.set_state(SpendMoney.amount.state)


async def amount_of_money(message: types.Message, state: FSMContext):
    try:
        amount = round(float(message.text), 2)
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.reply("Неверная сумма, введите число, например <b>20.55</b>", parse_mode=types.ParseMode.HTML)
        return
    await state.update_data(amount=amount)

    await state.set_state(SpendMoney.people.state)
    # TODO add list generator
    answer = "На кого делим? Выбери по-одному или всех сразу.\n"
    author_name = get_author_name(message.from_user.username)
    await message.answer(answer, reply_markup=names_keyboard(author_name))


async def share_money_spend(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    author_name = get_author_name(message.from_user.username)
    if user_data.get('people') is None:
        await state.update_data(people=[author_name])

    if message.text == "👨‍👨‍👦‍👦 На всех":
        await state.update_data(people=allowed_names.copy())
        await message.answer(
            "Вы выбрали <b>всех</b>. Перейти к следующему шагу?",
            parse_mode=types.ParseMode.HTML,
            reply_markup=names_keyboard(author_name)
        )

    elif message.text == "🗑️ Очистить":
        await state.update_data(people=[author_name])
        await message.answer(
            "Список <b>пуст</b>. Выберите снова.",
            parse_mode=types.ParseMode.HTML,
            reply_markup=names_keyboard(author_name)
        )

    elif message.text == "⏭️ Далее":
        user_data = await state.get_data()
        people = user_data.get('people')
        if people is None:
            await message.answer("Вы не добавили ни одного пользователя, попробуйте еще раз.")
            return
        await state.set_state(SpendMoney.comment.state)
        await message.answer("Добавьте комментарий.", reply_markup=cancel_keyboard())

    else:
        try:
            name = message.text
            if name not in allowed_names:
                raise ValueError
        except ValueError:
            await message.reply(
                "Неверное имя, попробуйте еще раз",
                reply_markup=names_keyboard(author_name)
            )
            return

        user_data = await state.get_data()
        people = set(user_data.get('people', []))
        people.add(name)
        await state.update_data(people=list(people))
        people_str = ', '.join(list(people))
        await message.answer(
            f"Вы добавили <b>{people_str}</b>. Продолжить?",
            parse_mode=types.ParseMode.HTML,
            reply_markup=names_keyboard(author_name)
        )


async def add_comment(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text)
    user_data = await state.get_data()
    count_users = len(user_data['people'])
    people_str = ", ".join(user_data['people'])
    amount_per_user = round(user_data['amount'] / count_users, 2)
    text = f"<u>Вы хотите добавить следующую запись:</u>\n\n" \
           f"Сумма: <b>{user_data['amount']}</b> лари\n\n" \
           f"Поделить на <b>{count_users}</b> человек:\n" \
           f"{people_str}\n\n" \
           f"По <b>{amount_per_user}</b> лари на каждого\n\n" \
           f"Комментарий:\n" \
           f"{user_data['comment']}"
    await message.answer(text, reply_markup=confirm_keyboard(), parse_mode=types.ParseMode.HTML)
    await state.set_state(SpendMoney.confirm.state)


async def save_result(message: types.Message, state: FSMContext):
    try:
        if message.text != "✅ Подтвердить":
            raise ValueError
    except ValueError:
        await message.reply("Выберите один из двух вариантов", reply_markup=confirm_keyboard())
        return
    user_data = await state.get_data()
    save_transaction_to_db(message.from_user.username, user_data)
    save_history_db(message.from_user.username, user_data)
    # TODO add notification
    user_name = get_author_name(message.from_user.username)
    notify = f"🛎️ <b>{user_name}</b> только что добавил новую запись в расходы:\n\n"\
             f"<b>Сумма:</b> {user_data['amount']} лари\n"\
             f"<b>Участники:</b>\n{', '.join(user_data['people'])}\n"\
             f"<b>Комментарий:</b>\n{user_data['comment']}\n\n"\
             f"Всем хорошего дня и не забывайте страдать 🫶"
    await bot.send_message(
        text=notify,
        chat_id=-1001979839596,
        disable_notification=True,
        parse_mode=types.ParseMode.HTML
    )
    await state.finish()
    await message.answer("Запись сохранена. Спасибо!", reply_markup=get_main_keyboard())


def register_state_handlers(dp: Dispatcher):
    dp.register_message_handler(
        cancel_handler,
        PrivateChatFilter(),
        content_types=['text'],
        text='❌ Отмена', state="*"
    )
    dp.register_message_handler(
        spend_money,
        PrivateChatFilter(),
        content_types=['text'],
        text='💸 Записать траты'
    )
    dp.register_message_handler(
        amount_of_money,
        PrivateChatFilter(),
        state=SpendMoney.amount
    )
    dp.register_message_handler(
        share_money_spend,
        PrivateChatFilter(),
        state=SpendMoney.people
    )
    dp.register_message_handler(
        add_comment,
        PrivateChatFilter(),
        state=SpendMoney.comment
    )
    dp.register_message_handler(
        save_result,
        PrivateChatFilter(),
        state=SpendMoney.confirm
    )
