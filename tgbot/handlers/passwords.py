from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from loader import dp
from tgbot.keyboards.inline.folders import folders_keyboard
from tgbot.keyboards.reply.folders import folders_keyboard as reply_fk
from tgbot.middlewares.authenticated import AuthMiddleware
from tgbot.misc.password_crypter import Crypter
from tgbot.models.supabase import SUPABASE_CLIENT
from tgbot.states.states import Password

router = Router()
router.message.filter(F.text)
router.message.middleware(AuthMiddleware())


@router.message(Command(commands=["passwords"]))
async def show_passwords(message: Message, client: SUPABASE_CLIENT):
    folders = client.get_all("Folders", conditions={"user": str(message.from_user.id)})
    keyboard = folders_keyboard(folders)
    return await message.answer("Click on the folders:", reply_markup=keyboard)


@router.message(Command(commands=["create_password", "cp"]))
async def create_password(message: Message, state: FSMContext):
    await state.set_state(Password.name)
    return await message.answer("Write name of the password")


@router.message(Password.name)
async def answer_name(message: Message, state: FSMContext):
    await state.update_data(password_name=message.text)
    await state.set_state(Password.description)
    return await message.answer("Write password description")


@router.message(Password.description)
async def answer_description(message: Message, state: FSMContext):
    await state.update_data(password_description=message.text)
    await state.set_state(Password.password)
    return await message.answer("Write password itself")


@router.message(Password.password)
async def answer_password(
    message: Message, state: FSMContext, client: SUPABASE_CLIENT, crypter: Crypter
):
    await state.update_data(password_code=crypter.encrypt(message.text))
    await state.set_state(Password.folder)
    keyboard = reply_fk(client, message.from_user.id)
    return await message.answer("Choose folder:", reply_markup=keyboard)


@router.message(Password.folder)
async def answer_password(message: Message, state: FSMContext, client: SUPABASE_CLIENT):
    user_data = await state.get_data()
    password = client.insert(
        "Passwords",
        {
            "name": user_data["password_name"],
            "description": user_data["password_description"],
            "user": str(message.from_user.id),
            "folder": message.text,
            "hashedPassword": user_data["password_code"],
        },
    )
    if password:
        await state.set_state(state=None)
        return await message.answer("You have successfully create the password")
    await state.set_state(Password.name)
    return await message.answer("Try again from the name:")


dp.include_router(router)
