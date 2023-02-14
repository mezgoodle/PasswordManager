from aiogram import F, Router, html
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from loader import dp
from tgbot.keyboards.inline.callbacks import PasswordsCallbackFactory
from tgbot.keyboards.inline.passwords import passwords_keyboard
from tgbot.keyboards.inline.question import question_keyboard
from tgbot.keyboards.reply.folders import folders_keyboard as reply_fk
from tgbot.middlewares.authenticated import AuthMiddleware
from tgbot.misc.password_crypter import Crypter
from tgbot.models.supabase import SUPABASE_CLIENT
from tgbot.states.states import Password, UpdatePassword

router = Router()
router.message.filter(F.text)
router.message.middleware(AuthMiddleware())

# TODO: handle empty records
@router.message(Command(commands=["passwords"]))
async def show_passwords(message: Message, client: SUPABASE_CLIENT, state: FSMContext):
    folders = client.get_all("Folders", conditions={"user": str(message.from_user.id)})
    keyboard = reply_fk(folders)
    await state.set_state("folder_name")
    return await message.answer("Click on the folders:", reply_markup=keyboard)


@router.message(StateFilter("folder_name"))
async def show_passwords_from_folder(
    message: Message, client: SUPABASE_CLIENT, state: FSMContext
):
    passwords = client.get_all(
        "Passwords",
        conditions={"user": str(message.from_user.id), "folder": message.text},
    )
    keyboard = passwords_keyboard(passwords)
    await state.set_state(state=None)
    return await message.answer("Here are your passwords:", reply_markup=keyboard)


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
    await state.update_data(password_code=str(crypter.encrypt(message.text)))
    await state.set_state(Password.folder)
    folders = client.get_all("Folders", conditions={"user": str(message.from_user.id)})
    keyboard = reply_fk(folders)
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


@router.message(UpdatePassword.name)
async def answer_update_name(message: Message, state: FSMContext):
    if message.text != "/pass":
        await state.update_data(password_name=message.text)
    await state.set_state(UpdatePassword.description)
    return await message.answer(
        "Write description of password or press /pass to left the previous value"
    )


@router.message(UpdatePassword.description)
async def answer_update_description(message: Message, state: FSMContext):
    if message.text != "/pass":
        await state.update_data(password_description=message.text)
    await state.set_state(UpdatePassword.password)
    return await message.answer(
        "Write password itself or press /pass to left the previous value"
    )


@router.message(UpdatePassword.password)
async def answer_update_password(
    message: Message, state: FSMContext, crypter: Crypter, client: SUPABASE_CLIENT
):
    if message.text != "/pass":
        await state.update_data(password_hashed=crypter.encrypt(message.text))
    await state.set_state(UpdatePassword.folder)
    folders = client.get_all("Folders", conditions={"user": str(message.from_user.id)})
    keyboard = reply_fk(folders)
    return await message.answer(
        "Choose folder name or press /pass to left the previous value",
        reply_markup=keyboard,
    )


@router.message(UpdatePassword.folder)
async def answer_update_folder(
    message: Message, state: FSMContext, client: SUPABASE_CLIENT
):
    if message.text != "/pass":
        await state.update_data(password_folder=message.text)
    user_data = await state.get_data()
    password = client.update(
        "Passwords",
        {
            "name": user_data["password_name"],
            "description": user_data["password_description"],
            "hashedPassword": user_data["password_hashed"],
            "folder": user_data["password_folder"],
        },
        "id",
        user_data["password_id"],
    )
    if password:
        await state.set_state(state=None)
        return await message.answer("You have successfully update the password")
    await state.set_state(UpdatePassword.name)
    return await message.answer("Try again from the name:")


@router.callback_query(PasswordsCallbackFactory.filter(F.action == "show"))
async def show_password(
    callback: CallbackQuery,
    callback_data: PasswordsCallbackFactory,
    crypter: Crypter,
    client: SUPABASE_CLIENT,
):
    password = client.get_single("Passwords", "id", callback_data.id)
    await callback.message.answer(
        f"Name: {html.bold(password['name'])}\nDescription: {html.bold(password['description'])}\nPassword: {html.bold(crypter.decrypt(password['hashedPassword']))}"
    )
    return await callback.answer()


@router.callback_query(PasswordsCallbackFactory.filter(F.action == "update"))
async def update_password(
    callback: CallbackQuery,
    callback_data: PasswordsCallbackFactory,
    state: FSMContext,
    client: SUPABASE_CLIENT,
):
    password = client.get_single("Passwords", "id", callback_data.id)
    await state.set_state(UpdatePassword.name)
    await state.update_data(
        {
            "password_name": password["name"],
            "password_description": password["description"],
            "password_id": password["id"],
            "password_hashed": password["hashedPassword"],
            "password_folder": password["folder"],
        }
    )
    await callback.message.answer(
        "Write new name of the password or press /pass to left the previous value",
    )
    return await callback.answer()


@router.callback_query(PasswordsCallbackFactory.filter(F.action == "delete"))
async def delete_password(
    callback: CallbackQuery, callback_data: PasswordsCallbackFactory, state: FSMContext
):
    await state.update_data({"delete_id": callback_data.id})
    keyboard = question_keyboard("Passwords")
    await callback.message.answer(
        f"Are you sure to delete {html.bold(callback_data.name)} password?",
        reply_markup=keyboard,
    )
    return await callback.answer()


dp.include_router(router)
