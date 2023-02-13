from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.keyboards.inline.callbacks import PasswordsCallbackFactory


def passwords_keyboard(passwords: List[dict]):
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
            callback_data=PasswordsCallbackFactory(id=password["id"], action="delete"),
        )
        # builder.button(
        #     text="Update",
        #     callback_data=PasswordsCallbackFactory(
        #         id=password["id"],
        #         action="update",
        #         name=password["name"],
        #         description=password["description"],
        #         password=password["hashedPassword"],
        #         folder=password["folder"],
        #     ),
        # )
    builder.adjust(3)
    return builder.as_markup()
