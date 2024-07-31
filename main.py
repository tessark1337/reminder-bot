import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

import handlers.user
from config_reader import config

async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()
    dp.include_routers(handlers.user.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())