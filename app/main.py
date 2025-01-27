import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import logging

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


bot = Bot(token=os.getenv('BOT_TOKEN'))

dp = Dispatcher()

@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.reply(f'Привет, {message.from_user.first_name}! Это простой бот, который отправляет текущую дату и время.')
    logger.info(f"Команда /start от пользователя {message.from_user.id}")
    

async def main():
    logger.info('Start...')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())