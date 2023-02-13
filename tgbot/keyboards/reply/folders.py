from typing import List

from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def folders_keyboard(folders: List[dict]):
    builder = ReplyKeyboardBuilder()
    for folder in folders:
        builder.add(KeyboardButton(text=str(folder["name"])))
    builder.adjust(4)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
