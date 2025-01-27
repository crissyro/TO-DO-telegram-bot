import asyncio
from aiogram import Dispatcher
from handlers.handlers import first_router
from config.config import Config

dp = Dispatcher()

async def main():
    Config.logger.info('Start...')
    dp.include_router(first_router)
    await Config.bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(Config.bot)

if __name__ == '__main__':
    asyncio.run(main())