from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hlink
from aiogram.fsm.state import State, StatesGroup

from keyboards.keyboards import back_keyboard, main_kb, deadline_keyboard
from config.config import Config
from database.database import add_task, get_tasks_with_numbers, delete_by_position
from datetime import datetime, timedelta

first_router = Router()

class TaskStates(StatesGroup):
    """
    @class TaskStates
    @brief Finite State Machine states for task management
    
    @var waiting_for_task_text: State for awaiting task description
    @var waiting_for_deadline: State for awaiting task deadline
    @var waiting_for_task_number: State for awaiting task number for deletion
    """
    waiting_for_task_text = State()
    waiting_for_deadline = State()
    waiting_for_custom_date = State()
    waiting_for_task_number = State()

async def set_bot_commands():
    """
    @fn set_bot_commands
    @brief Sets up bot commands menu
    
    Configures the list of available commands in the Telegram bot menu
    """
    await Config.bot.set_my_commands([
        types.BotCommand(command="/add", description="Add new task"),
        types.BotCommand(command="/list", description="Show all tasks"),
        types.BotCommand(command="/delete", description="Delete task by number"),
        types.BotCommand(command="/help", description="Show help"),
        types.BotCommand(command="/contribute", description="Contribute to project"),
        types.BotCommand(command="/review", description="Send feedback"),
        types.BotCommand(command="/donate", description="Support the project")
    ])

@first_router.message(CommandStart())
async def start_command(message: types.Message):
    """
    @fn start_command
    @brief Handles /start command
    
    @param message: Incoming message object
    """
    await message.answer(
        "📝 Welcome to the To-Do List bot!\n"
        "Use the menu on the left or the buttons below:",
        reply_markup=main_kb()
    )
    await set_bot_commands()

@first_router.message(Command('help'))
async def help_command(message: types.Message):
    """
    @fn help_command
    @brief Handles /help command
    
    @param message: Incoming message object
    """
    help_text = (
        "ℹ️ Available commands:\n"
        "/add - Add a new task\n"
        "/list - Show all tasks\n"
        "/delete - Delete task by number\n"
        "/help - Show this message\n"
        "/contribute - Contribute to project\n"
        "/review - Send feedback\n"
        "/donate - Support the project"
    )
    await message.answer(help_text)

@first_router.message(Command('add'))
async def add_task_command(message: types.Message, state: FSMContext):
    """
    @fn add_task_command
    @brief Initiates task creation flow
    
    @param message: Incoming message object
    @param state: Finite State Machine context
    """
    await message.answer("✏️ Please enter your task text:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(TaskStates.waiting_for_task_text)

@first_router.message(TaskStates.waiting_for_task_text)
async def process_task_text(message: types.Message, state: FSMContext):
    await state.update_data(task_text=message.text)
    await message.answer(
        "📅 Choose deadline:",
        reply_markup=deadline_keyboard()
    )
    await state.set_state(TaskStates.waiting_for_deadline)
    
@first_router.message(TaskStates.waiting_for_custom_date)
async def process_custom_date(message: types.Message, state: FSMContext):
    if message.text == "↩️ Back":
        await message.answer("📅 Choose deadline:", reply_markup=deadline_keyboard())
        await state.set_state(TaskStates.waiting_for_deadline)
        return

    try:
        deadline_date = datetime.strptime(message.text, "%d.%m.%Y").date()
        deadline = datetime.combine(deadline_date, datetime.max.time())
        
        if deadline.date() < datetime.now().date():
            raise ValueError("The date cannot be in the past")
            
        data = await state.get_data()
        await add_task(message.from_user.id, data['task_text'], deadline)
        await message.answer("✅ Task added!", reply_markup=main_kb())
        await state.clear()
        
    except ValueError as e:
        await message.answer(f"❌ Error: {str(e)}\nUse format DD.MM.YYYY")

@first_router.message(TaskStates.waiting_for_deadline)
async def process_deadline(message: types.Message, state: FSMContext):
    data = await state.get_data()
    
    try:
        if message.text == "Today 🕒":
            deadline = datetime.now().replace(hour=23, minute=59)
        elif message.text == "Tomorrow 📅":
            deadline = (datetime.now() + timedelta(days=1)).replace(hour=23, minute=59)
        elif message.text == "Custom date 📆":
            await message.answer(
                "⌨️ Please enter date and time in format:\nDD.MM.YYYY HH:MM\n"
                "Example: 31.12.2024",
                reply_markup=back_keyboard()
            )
            await state.set_state(TaskStates.waiting_for_custom_date)
            return
        else:
            await message.answer("⚠️ Please use the selection buttons")
            return

        await add_task(message.from_user.id, data['task_text'], deadline)
        await message.answer("✅ Task added successfully!", reply_markup=main_kb())
        await state.clear()
        
    except Exception as e:
        await message.answer("⚠️ Failed to save task. Please try again.")
        await state.clear()

@first_router.message(Command('list'))
async def list_tasks_command(message: types.Message):
    """
    @fn list_tasks_command
    @brief Displays user's tasks
    
    @param message: Incoming message object
    """
    try:
        tasks = await get_tasks_with_numbers(message.from_user.id)
        
        if not tasks:
            return await message.answer("📭 Your task list is empty!")
        
        tasks_text = []
        for num, task in tasks:
            status = "⏳" if task.deadline > datetime.now() else "❗️OVERDUE"
            tasks_text.append(
                f"{num}. {task.task}\n"
                f"   └─ Deadline: {task.deadline.strftime('%d.%m.%Y %H:%M')} {status}"
            )
        
        await message.answer(
            "📋 Your tasks:\n" + "\n\n".join(tasks_text),
            parse_mode="Markdown"
        )
    except Exception as e:
        await message.answer("❌ Failed to load tasks. Please try again.")

@first_router.message(Command('delete'))
async def delete_task_command(message: types.Message, state: FSMContext):
    """
    @fn delete_task_command
    @brief Initiates task deletion flow with back option
    
    @param message: Incoming message object
    @param state: Finite State Machine context
    """
    await message.answer(
        "❌ Enter task number to delete or click Back:",
        reply_markup=back_keyboard()
    )
    
    await state.set_state(TaskStates.waiting_for_task_number)
    
@first_router.message(TaskStates.waiting_for_task_number)
async def process_delete_task(message: types.Message, state: FSMContext):
    """
    @fn process_delete_task
    @brief Processes task deletion with enhanced error handling
    
    @param message: Incoming message object
    @param state: Finite State Machine context
    """
    if message.text == "↩️ Back":
        await message.answer("🏠 Returning to main menu.", reply_markup=main_kb())
        await state.clear()
        return

    try:
        position = int(message.text)
        if await delete_by_position(message.from_user.id, position):
            await message.answer("✅ Task deleted successfully!", reply_markup=main_kb())
            await state.clear()
        else:
            await message.answer(
                "❌ Task number not found! Please try again:",
                reply_markup=back_keyboard()
            )
    except ValueError:
        await message.answer(
            "⚠️ Please enter a valid number or click Back:",
            reply_markup=back_keyboard()
        )

GITHUB_URL = "https://github.com/crissyro/TO-DO-telegram-bot"
TELEGRAM_URL = "https://t.me/integral_cursed"

@first_router.message(Command('contribute'))
async def contribute_command(message: types.Message):
    """
    @fn contribute_command
    @brief Shows contribution information
    
    @param message: Incoming message object
    """
    github_link = hlink("GitHub Repository", GITHUB_URL)
    response = (f"🎉 Feel free to contribute to the project!\n"
                f"{github_link}\n\n"
                "Your contributions are always welcome! 🌟")
    await message.answer(response, parse_mode="HTML")

@first_router.message(Command('review'))
async def review_command(message: types.Message):
    """
    @fn review_command
    @brief Provides feedback contact information
    
    @param message: Incoming message object
    """
    telegram_link = hlink("Contact Author", TELEGRAM_URL)
    response = (f"📮 Send your feedback directly to the author:\n"
                f"{telegram_link}\n\n"
                "Your opinion matters! 💌")
    await message.answer(response, parse_mode="HTML")

@first_router.message(Command('donate'))
async def donate_command(message: types.Message):
    """
    @fn donate_command
    @brief Shows donation information
    
    @param message: Incoming message object
    """
    response = ("❤️ Thank you for wanting to support the project!\n\n"
                "Currently we don't accept donations, but your active "
                "use of the bot is the best reward! 🚀")
    await message.answer(response)