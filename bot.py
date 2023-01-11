import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types.webhook_info import WebhookInfo
from loguru import logger

from loader import bot, dp
from tgbot.config import Settings, config
from tgbot.services.admins_notify import on_startup_notify
from tgbot.services.setting_commands import set_default_commands


def register_all_middlewares(dp: Dispatcher, config: Settings):
    logger.info("Registering middlewares")


def register_all_handlers(dispatcher: Dispatcher) -> None:
    from tgbot import handlers

    logger.info("Registering handlers")


async def on_startup(
    dispatcher: Dispatcher, bot: Bot, config: Settings, webhook_url: str = None
) -> None:
    register_all_middlewares(dispatcher, config)
    register_all_handlers(dispatcher)
    await on_startup_notify(bot)
    await set_default_commands(bot)
    # Get current webhook status
    webhook: WebhookInfo = await bot.get_webhook_info()

    if webhook_url:
        await bot.set_webhook(webhook_url)
        logger.info("Webhook was set")
    elif webhook.url:
        await bot.delete_webhook()
        logger.info("Webhook was deleted")

    logger.info("Bot started")


async def main():
    logger.add(
        "tgbot.log",
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {file} | {function}, {line} | {message}",
        rotation="10 KB",
        compression="zip",
    )
    logger.info("Starting bot")

    await on_startup(dp, bot, config)
    await dp.start_polling(
        bot, allowed_updates=dp.resolve_used_update_types(), config=config
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot shutdown!")
