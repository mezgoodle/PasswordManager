from aiogram import F, Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from loader import dp
from tgbot.models.supabase import SUPABASE_CLIENT

router = Router()
router.message.filter(F.text)

# TODO: clean here
@router.message(CommandStart())
async def answer_start(message: Message):
    return await message.answer("start command")


@router.message(Command(commands=["cancel"]))
@router.message(Text(text="cancel", ignore_case=True))
async def cancel_state(message: Message, state: FSMContext):
    await state.set_state(state=None)
    await message.answer(text="Action is canceled", reply_markup=ReplyKeyboardRemove())


@router.message(Command(commands=["help"]))
async def help_command(message: Message):
    return await message.answer("help command")


dp.include_router(router)
