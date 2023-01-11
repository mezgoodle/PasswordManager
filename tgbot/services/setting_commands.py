from aiogram import Bot
from aiogram.types import BotCommand
from loguru import logger


async def set_default_commands(bot: Bot) -> None:
    logger.info("Start admins notification")
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="Show help"),
        BotCommand(command="folders", description="Show folders"),
        BotCommand(command="passwords", description="Show passwords"),
    ]
    await bot.set_my_commands(commands=commands)
