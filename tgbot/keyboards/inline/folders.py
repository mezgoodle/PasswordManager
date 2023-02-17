from typing import List

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.keyboards.inline.callbacks import (
    FoldersCallbackFactory,
    PagesCallbackFactory,
)


def folders_keyboard(folders: List[dict], count: int, page: int = 1):
    per_page = 5
    folders = folders[per_page * (page - 1) : per_page * page]
    builder = InlineKeyboardBuilder()
    for folder in folders:
        builder.button(
            text=folder["name"],
            callback_data=FoldersCallbackFactory(
                id=folder["id"],
                action="show",
                name=folder["name"],
                description=folder["description"],
            ),
        )
        builder.button(
            text="Delete",
            callback_data=FoldersCallbackFactory(
                id=folder["id"], action="delete", name=folder["name"]
            ),
        )
        builder.button(
            text="Update",
            callback_data=FoldersCallbackFactory(
                id=folder["id"],
                action="update",
                name=folder["name"],
                description=folder["description"],
            ),
        )
    builder.button(
        text="Previous <<",
        callback_data=PagesCallbackFactory(page=page - 1, type="folders"),
    ) if per_page * (page - 1) != 0 else None
    builder.button(text="Page", callback_data="Nothing")
    builder.button(
        text=">> Next",
        callback_data=PagesCallbackFactory(page=page + 1, type="folders"),
    ) if per_page * page < count else None
    builder.adjust(3)
    return builder.as_markup()
