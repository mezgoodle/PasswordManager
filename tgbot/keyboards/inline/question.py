from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.keyboards.inline.callbacks import QuestionCallbackFactory


def question_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Yes", callback_data=QuestionCallbackFactory(answer=True))
    builder.button(text="No", callback_data=QuestionCallbackFactory(answer=False))
    builder.adjust(2)
    return builder.as_markup()
