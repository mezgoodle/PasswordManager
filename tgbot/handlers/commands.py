from aiogram import F, Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from loader import dp
from tgbot.middlewares.authenticated import AuthMiddleware
from tgbot.models.supabase import SUPABASE_CLIENT

router = Router()
router.message.filter(F.text)
router.message.middleware(AuthMiddleware())


@router.message(CommandStart())
async def answer_start(message: Message, client: SUPABASE_CLIENT):
    # result = client.insert(
    #     "Users",
    #     {
    #         "username": message.from_user.username + "1",
    #         "telegram_id": str(message.from_user.id) + "1",
    #     },
    # )
    # assert result
    return await message.answer("start command")


@router.message(Command(commands=["cancel"]))
@router.message(Text(text="cancel", ignore_case=True))
async def cancel_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Action is canceled", reply_markup=ReplyKeyboardRemove())


@router.message(Command(commands=["help"]))
async def help_command(message: Message, client: SUPABASE_CLIENT):
    result = client.get_all("Users", "username, telegram_id")
    print(result)
    result = client.get_single("Users", "username", "sylvenis")
    print(result)
    return await message.answer("help command")


@router.message(Command(commands=["passwords"]))
async def passwords_command(message: Message, client: SUPABASE_CLIENT):
    result = client.update("Users", {"username": "sylvenis"}, "username", "sylvenis")
    print(result)
    return await message.answer("passwords")


@dp.message(Command(commands=["folders"]))
async def folders_command(message: Message, client: SUPABASE_CLIENT):
    result = client.delete("Users", "username", "sylvenis1")
    print(result)
    return await message.answer("folders command")


dp.include_router(router)
