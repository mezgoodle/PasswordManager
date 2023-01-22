from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from loader import dp
from tgbot.middlewares.authenticated import AuthMiddleware
from tgbot.models.supabase import SUPABASE_CLIENT
from tgbot.states.states import Folder

router = Router()
router.message.filter(F.text)
router.message.middleware(AuthMiddleware())


@router.message(Command(commands=["folders"]))
async def show_folders(message: Message, client: SUPABASE_CLIENT):
    folders = client.get_all("Folders", column="user", value=str(message.from_user.id))
    print(folders)
    return await message.answer("Your folders:")


@router.message(Command(commands=["create_folder", "cf"]))
async def create_folder(message: Message, state: FSMContext):
    await state.set_state(Folder.name)
    return await message.answer("Write name of folder")


@router.message(Folder.name)
async def answer_name(message: Message, state: FSMContext):
    await state.update_data(folder_name=message.text.lower())
    await state.set_state(Folder.description)
    return await message.answer("Write description of folder")


@router.message(Folder.description)
async def answer_description(
    message: Message, state: FSMContext, client: SUPABASE_CLIENT
):
    user_data = await state.get_data()
    folder = client.insert(
        "Folders",
        {
            "name": user_data["folder_name"],
            "description": message.text.lower(),
            "user": str(message.from_user.id),
        },
    )
    if folder:
        await state.set_state(state=None)
        return await message.answer("Write description of folder")
    await state.set_state(Folder.name)
    return await message.answer("Try again from the name:")


dp.include_router(router)
