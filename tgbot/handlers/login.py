from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from loader import dp
from tgbot.models.supabase import SUPABASE_CLIENT
from tgbot.states.states import UserCredentials

router = Router()
router.message.filter(F.text)


@router.message(Command(commands=["login", "log", "l"]))
async def start_login(message: Message, state: FSMContext):
    await state.set_state(UserCredentials.email)
    return await message.answer(
        "You have started your login process. Enter your email."
    )


@router.message(UserCredentials.email)
async def answer_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text.lower())
    await state.set_state(UserCredentials.password)
    await message.answer("Now enter your password")


@router.message(UserCredentials.password)
async def answer_password(message: Message, state: FSMContext, client: SUPABASE_CLIENT):
    user_data = await state.get_data()
    await state.set_state(state=None)
    token = client.sign_in(user_data["email"], message.text.lower())
    print(token)
    await state.update_data(token=token)
    return await message.answer("You have successfully logged in.")


@router.message(UserCredentials.password)
async def wrong_answer_password(message: Message):
    return await message.answer("Your password must have length more than five.")


dp.include_router(router)
