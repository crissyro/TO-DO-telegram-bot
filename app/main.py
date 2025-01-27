import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
import logging

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


bot = Bot(token=os.getenv('BOT_TOKEN'))

dp = Dispatcher()

@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.reply("📝 Добро пожаловать в To-Do List бот!\n"
                        "Используйте команды:\n"
                        "/add - добавить задачу\n"
                        "/list - показать список задач\n"
                        "/delete - удалить задачу\n"
                        "/help - справка")
    
    logger.info(f"Команда /start от пользователя {message.from_user.id}")
    
@dp.message(Command('help'))
async def help_command(message: types.Message):
    await message.reply("ℹ️ Доступные команды:\n"
                        "/add - добавить новую задачу\n"
                        "/list - показать все задачи\n"
                        "/delete - удалить задачу по номеру\n"
                        "/help - показать это сообщение")
    
    logger.info(f"Команда /help от пользователя {message.from_user.id}")

async def main():
    logger.info('Start...')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())