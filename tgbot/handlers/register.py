from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from loader import dp
from tgbot.models.supabase import SUPABASE_CLIENT
from tgbot.states.states import Register

router = Router()
router.message.filter(F.text)


@router.message(Command(commands=["reg", "register", "r"]))
async def start_register(message: Message, state: FSMContext):
    await state.set_state(Register.email)
    return await message.answer(
        "You have started your registration process. Enter your working email."
    )


@router.message(Register.email)
async def answer_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text.lower())
    await state.set_state(Register.password)
    await message.answer("Now enter your password. Minimum 6 characters.")


@router.message(Register.password, F.text.len() > 5)
async def answer_password(message: Message, state: FSMContext, client: SUPABASE_CLIENT):
    user_data = await state.get_data()
    await state.clear()
    print(user_data)
    user = client.sign_up(user_data["email"], message.text.lower())
    print(user)
    return await message.answer("Now enter your password. Minimum 6 characters.")


@router.message(Register.password)
async def wrong_answer_password(message: Message):
    return await message.answer("Your password must have length more than five.")


dp.include_router(router)
