from typing import Optional

from aiogram.filters.callback_data import CallbackData


class FoldersCallbackFactory(CallbackData, prefix="folder"):
    id: str
    action: str
    name: Optional[str]
    description: Optional[str]


class PasswordsCallbackFactory(CallbackData, prefix="password"):
    id: str
    action: str
    name: Optional[str]


class QuestionCallbackFactory(CallbackData, prefix="question"):
    answer: bool
    object_type: str


class PagesCallbackFactory(CallbackData, prefix="page"):
    page: int
    type: str
    folder: Optional[str]
