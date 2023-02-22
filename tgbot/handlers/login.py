from aiogram import F, Router, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from loader import dp
from tgbot.models.supabase import SUPABASE_CLIENT
from tgbot.states.states import UserCredentials

router = Router()
router.message.filter(F.text)


@router.message(Command(commands=["login", "log", "l"]))
async def start_login(message: Message, state: FSMContext):
    user_data = await state.get_data()
    try:
        _ = user_data["token"]
        return await message.answer(html.bold("You have already logged in"))
    except KeyError:
        await state.set_state(UserCredentials.email)
        return await message.answer(
            "You have started your login process. Enter your email."
        )


@router.message(UserCredentials.email)
async def answer_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text.lower())
    await state.set_state(UserCredentials.password)
    return await message.answer("Now enter your password")


@router.message(UserCredentials.password)
async def answer_password(
    message: Message,
    state: FSMContext,
    client: SUPABASE_CLIENT,
    scheduler: AsyncIOScheduler,
):
    user_data = await state.get_data()
    await state.set_state(state=None)
    token = await client.sign_in(user_data["email"], message.text.lower())
    await state.update_data(token=token)
    scheduler.add_job(client.sign_out, "interval", minutes=5, args=(state,))
    return await message.answer(
        "You have successfully logged in. You will be automatically sing out after 5 minutes."
    )


@router.message(UserCredentials.password)
async def wrong_answer_password(message: Message):
    return await message.answer("Your password must have length more than five.")


dp.include_router(router)
