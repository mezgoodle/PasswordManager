from aiogram import F, Router, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from loader import dp
from tgbot.keyboards.inline.callbacks import (
    FoldersCallbackFactory,
    QuestionCallbackFactory,
)
from tgbot.keyboards.inline.folders import folders_keyboard
from tgbot.keyboards.inline.question import question_keyboard
from tgbot.middlewares.authenticated import AuthMiddleware
from tgbot.models.supabase import SUPABASE_CLIENT
from tgbot.states.states import Folder, UpdateFolder

router = Router()
router.message.filter(F.text)
router.message.middleware(AuthMiddleware())


@router.message(Command(commands=["folders"]))
async def show_folders(message: Message, client: SUPABASE_CLIENT):
    folders = client.get_all("Folders", column="user", value=str(message.from_user.id))
    keyboard = folders_keyboard(folders)
    return await message.answer("Your folders:", reply_markup=keyboard)


@router.message(Command(commands=["create_folder", "cf"]))
async def create_folder(message: Message, state: FSMContext):
    await state.set_state(Folder.name)
    return await message.answer("Write name of folder")


@router.message(Folder.name)
async def answer_name(message: Message, state: FSMContext):
    print("hello 2")
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
        return await message.answer("You have successfully create the folder")
    await state.set_state(Folder.name)
    return await message.answer("Try again from the name:")


@router.message(UpdateFolder.name)
async def answer_update_name(message: Message, state: FSMContext):
    print("hello 1")
    if message.text != "/pass":
        await state.update_data(folder_name=message.text.lower())
    await state.set_state(UpdateFolder.description)
    return await message.answer(
        "Write description of folder or press /pass to left the previous value"
    )


@router.message(UpdateFolder.description)
async def answer_update_description(
    message: Message, state: FSMContext, client: SUPABASE_CLIENT
):
    user_data = await state.get_data()
    folder = client.update(
        "Folders",
        {
            "name": user_data["folder_name"],
            "description": message.text.lower()
            if message.text != "/pass"
            else user_data["folder_description"],
        },
        "id",
        user_data["folder_id"],
    )
    if folder:
        await state.set_state(state=None)
        return await message.answer("You have successfully update the folder")
    await state.set_state(UpdateFolder.name)
    return await message.answer("Try again from the name:")


@router.callback_query(FoldersCallbackFactory.filter(F.action == "show"))
async def show_folder(
    callback: CallbackQuery,
    callback_data: FoldersCallbackFactory,
):
    await callback.message.answer(
        f"Name: {html.bold(callback_data.name)}\nDescription: {html.bold(callback_data.description)}"
    )
    return await callback.answer()


@router.callback_query(FoldersCallbackFactory.filter(F.action == "delete"))
async def delete_folder(
    callback: CallbackQuery, callback_data: FoldersCallbackFactory, state: FSMContext
):
    await state.update_data({"folder_id": callback_data.id})
    keyboard = question_keyboard()
    await callback.message.answer(
        f"Are you sure to delete {html.bold(callback_data.name)} folder?",
        reply_markup=keyboard,
    )
    return await callback.answer()


@router.callback_query(FoldersCallbackFactory.filter(F.action == "update"))
async def update_folder(
    callback: CallbackQuery, callback_data: FoldersCallbackFactory, state: FSMContext
):
    await state.set_state(UpdateFolder.name)
    await state.update_data(
        {
            "folder_name": callback_data.name,
            "folder_description": callback_data.description,
            "folder_id": callback_data.id,
            "type": "update",
        }
    )
    await callback.message.answer(
        "Write new name of the folder or press /pass to left the previous value",
    )
    return await callback.answer()


@router.callback_query(QuestionCallbackFactory.filter())
async def delete_folder_answer(
    callback: CallbackQuery,
    callback_data: QuestionCallbackFactory,
    state: FSMContext,
    client: SUPABASE_CLIENT,
):
    data = await state.get_data()
    if callback_data.answer:
        client.delete("Folders", "id", data["folder_id"])
        await state.update_data({"folder_id": None})
        await callback.message.answer(f"Folder has been deleted")
    return await callback.answer()


dp.include_router(router)
