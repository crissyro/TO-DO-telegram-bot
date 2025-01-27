from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hlink
from aiogram.fsm.state import State, StatesGroup

from keyboards.keyboards import main_kb
from config.config import Config
from database.database import add_task, get_all_tasks, delete_task  
from datetime import datetime, timedelta

first_router = Router()

class TaskStates(StatesGroup):
    waiting_for_task_text = State()
    waiting_for_deadline = State()

class AddTaskState(StatesGroup):
    waiting_for_task_text = State()

class DeleteTaskState(StatesGroup):
    waiting_for_task_id = State()

async def set_bot_commands():
    await Config.bot.set_my_commands([
        types.BotCommand(command="/contribute", description="Contributing into project-github repository"),
        types.BotCommand(command="/review", description="Send a review to author"),
        types.BotCommand(command="/donate", description="Donate"),
    ])

@first_router.message(CommandStart())
async def start_command(message: types.Message):
    """Handle /start command"""
    await message.answer(
        "📝 Welcome to the To-Do List bot!\n"
        "Use the menu on the left or the button below:",
        reply_markup=main_kb()
    )
    await set_bot_commands()
    Config.logger.info(f"/start command from user {message.from_user.id}")

@first_router.message(Command('help'))
async def help_command(message: types.Message):
    """Handle /help command"""
    help_text = (
        "ℹ️ Available commands:\n"
        "/add - Add a new task\n"
        "/list - Show all tasks\n"
        "/delete - Delete task by ID\n"
        "/help - Show this message\n"
        "/contribute - Contribute to project\n"
        "/review - Send feedback\n"
        "/donate - Support the project"
    )
    await message.answer(help_text)
    Config.logger.info(f"/help command from user {message.from_user.id}")

@first_router.message(Command('add'))
async def add_task_command(message: types.Message, state: FSMContext):
    """Handle /add command and initiate task creation flow"""
    await message.answer("✏️ Please enter your task text:")
    await state.set_state(AddTaskState.waiting_for_task_text)
    Config.logger.info(f"/add command from user {message.from_user.id}")
    
@first_router.message(AddTaskState.waiting_for_task_text)
async def process_task_text(message: types.Message, state: FSMContext):
    """Process task text input and save to database"""
    user_id = message.from_user.id
    task_text = message.text
    
    try:
        if len(task_text) > 500:
            raise ValueError("Task text too long (max 500 characters)")
            
        success = await add_task(user_id, task_text)
        
        if success:
            await message.answer("✅ Task added successfully!", reply_markup=main_kb())
            Config.logger.info(f"New task added by user {user_id}")
        else:
            await message.answer("❌ Failed to save task. Please try again.")
            
    except ValueError as ve:
        await message.answer(f"❌ Validation error: {str(ve)}")
        Config.logger.warning(f"Validation error for user {user_id}: {str(ve)}")
        
    except Exception as e:
        error_msg = "⚠️ Database error. Please try again later."
        await message.answer(error_msg)
        Config.logger.error(f"DB Error for user {user_id}: {str(e)}")
        Config.logger.exception(e)
    
    await state.clear()

@first_router.message(Command('list'))
async def list_tasks_command(message: types.Message):
    """Handle /list command and show user's tasks"""
    user_id = message.from_user.id
    
    try:
        tasks = await get_all_tasks(user_id)
        if not tasks:
            await message.answer("📭 Your task list is empty!")
            return
            
        tasks_list = "\n".join([f"{task.id}. {task.task}" for task in tasks])
        await message.answer(f"📋 Your tasks:\n{tasks_list}")
        Config.logger.info(f"Task list viewed by user {user_id}")
        
    except Exception as e:
        await message.answer("❌ Error retrieving tasks. Please try again.")
        Config.logger.error(f"Error retrieving tasks for user {user_id}: {str(e)}")

@first_router.message(Command('delete'))
async def delete_task_command(message: types.Message, state: FSMContext):
    """Handle /delete command and initiate task deletion flow"""
    await message.answer("❌ Enter the ID of the task you want to delete:")
    await state.set_state(DeleteTaskState.waiting_for_task_id)
    Config.logger.info(f"/delete command from user {message.from_user.id}")

@first_router.message(DeleteTaskState.waiting_for_task_id)
async def process_task_id(message: types.Message, state: FSMContext):
    """Process task ID input and delete from database"""
    user_id = message.from_user.id
    task_id = message.text
    
    try:
        task_id = int(task_id)
        success = await delete_task(task_id, user_id)
        
        if success:
            await message.answer("🗑 Task deleted successfully!", reply_markup=main_kb())
            Config.logger.info(f"Task {task_id} deleted by user {user_id}")
        else:
            await message.answer("⚠️ Task not found or permission denied!")
            Config.logger.warning(f"Failed deletion attempt by user {user_id} for task {task_id}")
            
    except ValueError:
        await message.answer("⚠️ Invalid input! Please enter a numeric task ID.")
        Config.logger.warning(f"Invalid task ID input by user {user_id}: {task_id}")
    except Exception as e:
        await message.answer("❌ Error deleting task. Please try again.")
        Config.logger.error(f"Error deleting task for user {user_id}: {str(e)}")
    
    await state.clear()
    
GITHUB_URL = "https://github.com/crissyro/TO-DO-telegram-bot"
TELEGRAM_URL = "https://t.me/integral_cursed"

@first_router.message(Command('contribute'))
async def contribute_command(message: types.Message):
    """Handle /contribute command"""
    github_link = hlink("GitHub Repository", GITHUB_URL)
    response = (f"🎉 Feel free to contribute to the project!\n"
                f"{github_link}\n\n"
                "Your contributions are always welcome! 🌟")
    await message.answer(response, parse_mode="HTML")
    Config.logger.info(f"/contribute command from {message.from_user.id}")

@first_router.message(Command('review'))
async def review_command(message: types.Message):
    """Handle /review command"""
    telegram_link = hlink("Contact Author", TELEGRAM_URL)
    response = (f"📮 Send your feedback directly to the author:\n"
                f"{telegram_link}\n\n"
                "Your opinion matters! 💌")
    await message.answer(response, parse_mode="HTML")
    Config.logger.info(f"/review command from {message.from_user.id}")

@first_router.message(Command('donate'))
async def donate_command(message: types.Message):
    """Handle /donate command (placeholder)"""
    response = ("❤️ Thank you for wanting to support the project!\n\n"
                "Currently we don't accept donations, but your active "
                "use of the bot is the best reward! 🚀")
    await message.answer(response)
    Config.logger.info(f"/donate command from {message.from_user.id}")