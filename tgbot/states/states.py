from aiogram.fsm.state import State, StatesGroup


class Register(StatesGroup):
    email = State()
    password = State()
