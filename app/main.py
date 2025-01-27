import asyncio
from aiogram import Dispatcher, types
from aiogram.filters import CommandStart, Command
from config.config import Config

dp = Dispatcher()

async def set_bot_commands():
    await Config.bot.set_my_commands([
        types.BotCommand(command="/add", description="Добавить задачу"),
        types.BotCommand(command="/list", description="Список задач"),
        types.BotCommand(command="/delete", description="Удалить задачу"),
        types.BotCommand(command="/help", description="Помощь"),
    ])

@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.reply("📝 Добро пожаловать в To-Do List бот!\n"
                        "Используйте команды:\n"
                        "/add - добавить задачу\n"
                        "/list - показать список задач\n"
                        "/delete - удалить задачу\n"
                        "/help - справка")
    await set_bot_commands()
    Config.logger.info(f"Команда /start от пользователя {message.from_user.id}")
    
@dp.message(Command('help'))
async def help_command(message: types.Message):
    await message.reply("ℹ️ Доступные команды:\n"
                        "/add - добавить новую задачу\n"
                        "/list - показать все задачи\n"
                        "/delete - удалить задачу по номеру\n"
                        "/help - показать это сообщение")
    Config.logger.info(f"Команда /help от пользователя {message.from_user.id}")
    
async def main():
    Config.logger.info('Start...')
    await Config.bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(Config.bot)

if __name__ == '__main__':
    asyncio.run(main())