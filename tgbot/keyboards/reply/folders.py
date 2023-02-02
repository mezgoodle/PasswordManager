from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from tgbot.models.supabase import SUPABASE_CLIENT


def folders_keyboard(client: SUPABASE_CLIENT, user_id: str):
    folders = client.get_all("Folders", "name", {"user": user_id})
    builder = ReplyKeyboardBuilder()
    for folder in folders:
        builder.add(KeyboardButton(text=str(folder["name"])))
    builder.adjust(4)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
