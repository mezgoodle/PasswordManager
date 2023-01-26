from typing import List

from aiogram import Bot
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def folders_keyboard(folders: List[dict]):
    builder = InlineKeyboardBuilder()
    for folder in folders:
        builder.button(text=folder["name"], callback_data=folder["name"])
        builder.button(text="Delete", callback_data=folder["name"])
        builder.button(text="Update", callback_data=folder["name"])
    builder.adjust(3)
    return builder.as_markup()
