from typing import Optional

from aiogram.filters.callback_data import CallbackData


class FoldersCallbackFactory(CallbackData, prefix="folder"):
    id: str
    action: str
    name: Optional[str]
    description: Optional[str]


class QuestionCallbackFactory(CallbackData, prefix="question"):
    answer: bool
