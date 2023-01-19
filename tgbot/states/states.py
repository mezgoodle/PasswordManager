from aiogram.fsm.state import State, StatesGroup


class UserCredentials(StatesGroup):
    email = State()
    password = State()
