from aiogram.fsm.state import State, StatesGroup


class UserCredentials(StatesGroup):
    email = State()
    password = State()


class Folder(StatesGroup):
    name = State()
    description = State()


class UpdateFolder(StatesGroup):
    name = State()
    description = State()


class Password(StatesGroup):
    name = State()
    password = State()
    folder = State()
