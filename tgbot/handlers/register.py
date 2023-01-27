from aiogram import F, Router, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from loader import dp
from tgbot.models.supabase import SUPABASE_CLIENT
from tgbot.states.states import UserCredentials

router = Router()
router.message.filter(F.text)


@router.message(Command(commands=["reg", "register", "r"]))
async def start_register(message: Message, state: FSMContext):
    user_data = await state.get_data()
    try:
        _ = user_data["token"]
        return await message.answer(html.bold("You have already logged in"))
    except KeyError:
        await state.set_state(UserCredentials.email)
        return await message.answer(
            "You have started your registration process. Enter your working email."
        )


@router.message(UserCredentials.email)
async def answer_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text.lower())
    await state.set_state(UserCredentials.password)
    await message.answer("Now enter your password. Minimum 6 characters.")


@router.message(UserCredentials.password, F.text.len() > 5)
async def answer_password(message: Message, state: FSMContext, client: SUPABASE_CLIENT):
    user_data = await state.get_data()
    await state.set_state(state=None)
    print(user_data)
    user = client.sign_up(user_data["email"], message.text.lower())
    print(user)
    return await message.answer("Now you have to confirm your email.")


@router.message(UserCredentials.password)
async def wrong_answer_password(message: Message):
    return await message.answer(
        "Your password must have length more than five. Try again"
    )


dp.include_router(router)
