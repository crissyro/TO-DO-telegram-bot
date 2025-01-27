from aiogram import F
from aiogram import Router, types
from aiogram.filters import CommandStart, Command

from keyboards.keyboards import main_kb
from config.config import Config

first_router = Router()

async def set_bot_commands():
    await Config.bot.set_my_commands([
        types.BotCommand(command="/contribute", description="Contributing into project-github repository"),
        types.BotCommand(command="/review", description="Send a review to author"),
        types.BotCommand(command="/donate", description="Donate"),
    ])

@first_router.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer(
        "📝 Welcome to the To-Do List bot!\n"
        "Use the menu on the left or the button below:",
        reply_markup=main_kb()
    )
    await set_bot_commands()
    Config.logger.info(f"Команда /start от пользователя {message.from_user.id}")
    
@first_router.message(Command('help'))
async def help_command(message: types.Message):
    await message.answer("ℹ️ Available commands:\n:\n"
                        "/add - add a new task\n"
                        "/list - show all tasks\n"
                        "/delete - delete task by number\n"
                        "/help - show this message")
    Config.logger.info(f"Команда /help от пользователя {message.from_user.id}")