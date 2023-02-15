from aiogram import F, Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from loader import dp

router = Router()
router.message.filter(F.text)


@router.message(CommandStart())
async def answer_start(message: Message):
    return await message.answer(
        "Welcome to the PasswordManager. To store your passwords you need to register in the system. Use command /r. For more command use /help."
    )


@router.message(Command(commands=["cancel"]))
@router.message(Text(text="cancel", ignore_case=True))
async def cancel_state(message: Message, state: FSMContext):
    await state.set_state(state=None)
    await message.answer(text="Action is canceled", reply_markup=ReplyKeyboardRemove())


@router.message(Command(commands=["help"]))
async def help_command(message: Message):
    return await message.answer(
        "/r - register\n/l - login\n/passwords - passwords\n/folders - folders\n/cp - create password\n/cf - create folder"
    )


dp.include_router(router)
