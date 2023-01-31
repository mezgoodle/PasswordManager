from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.keyboards.inline.callbacks import FoldersCallbackFactory


def folders_keyboard(folders: List[dict]):
    builder = InlineKeyboardBuilder()
    for folder in folders:
        builder.button(
            text=folder["name"],
            callback_data=FoldersCallbackFactory(
                id=folder["id"], action="show", name=folder["name"]
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
                id=folder["id"], action="update", name=folder["name"]
            ),
        )
    builder.adjust(3)
    return builder.as_markup()
