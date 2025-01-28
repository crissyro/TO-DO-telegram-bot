import asyncio
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.handlers import first_router
from config.config import Config
from database.database import init_db

async def on_startup():
    """Initialize database and perform startup actions"""
    await init_db()
    await Config.bot.delete_webhook(drop_pending_updates=True)
    
async def on_shutdown(dp: Dispatcher):
    """Handle graceful shutdown"""
    await dp.storage.close()
    await Config.bot.session.close()

async def main():
    """Main application entry point"""
    dp = Dispatcher(storage=MemoryStorage())
    
    dp.include_router(first_router)
    
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    try:
        await dp.start_polling(Config.bot)
    finally:
        await on_shutdown(dp)

if __name__ == '__main__':
    asyncio.run(main())