from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.keyboards.inline.callbacks import (
    PagesCallbackFactory,
    PasswordsCallbackFactory,
)


def passwords_keyboard(
    passwords: List[dict],
    count: int,
    folder: str,
    page: int = 1,
):
    per_page = 5
    passwords = passwords[per_page * (page - 1) : per_page * page]
    builder = InlineKeyboardBuilder()
    for password in passwords:
        builder.button(
            text=password["name"],
            callback_data=PasswordsCallbackFactory(
                id=password["id"],
                action="show",
            ),
        )
        builder.button(
            text="Delete",
            callback_data=PasswordsCallbackFactory(
                id=password["id"], action="delete", name=password["name"]
            ),
        )
        builder.button(
            text="Update",
            callback_data=PasswordsCallbackFactory(
                id=password["id"],
                action="update",
            ),
        )
    builder.button(
        text="Previous <<",
        callback_data=PagesCallbackFactory(
            page=page - 1, type="passwords", folder=folder
        ),
    ) if per_page * (page - 1) != 0 else None
    builder.button(text="Page", callback_data="Nothing")
    builder.button(
        text=">> Next",
        callback_data=PagesCallbackFactory(
            page=page + 1, type="passwords", folder=folder
        ),
    ) if per_page * page < count else None
    builder.adjust(3)
    return builder.as_markup()
