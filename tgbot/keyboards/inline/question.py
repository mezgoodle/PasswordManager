from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.keyboards.inline.callbacks import QuestionCallbackFactory


def question_keyboard(type: str):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Yes", callback_data=QuestionCallbackFactory(answer=True, type=type)
    )
    builder.button(
        text="No", callback_data=QuestionCallbackFactory(answer=False, type=type)
    )
    builder.adjust(2)
    return builder.as_markup()
