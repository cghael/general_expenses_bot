from aiogram.dispatcher.filters.state import StatesGroup, State


class SpendMoney(StatesGroup):
    amount = State()
    people = State()
    comment = State()
    confirm = State()
    notify = State()


class AdminState(StatesGroup):
    admin_menu = State()
    read_users_in_group = State()
    add_user_to_db = State()
    confirm = State()
    notify = State()
