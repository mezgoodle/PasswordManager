from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        state = data["state"]
        user_data = await state.get_data()
        try:
            _ = user_data["token"]
            return await handler(event, data)
        except KeyError:
            return await event.answer("You need to log in. Enter /l.")
