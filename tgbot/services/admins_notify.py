from aiogram import Bot
from loguru import logger

from tgbot.config import config


async def on_startup_notify(bot: Bot):
    logger.info("Start admins notification")

    admins = config.admins

    for admin in admins:
        try:
            await bot.send_message(
                admin, "Bot has been started", disable_notification=True
            )
        except:
            logger.debug(f"Chat with {admin} not found")
