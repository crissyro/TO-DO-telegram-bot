from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_kb() -> ReplyKeyboardMarkup:
    
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="/add"),
        KeyboardButton(text="/list")
    )
    builder.row(
        KeyboardButton(text="/delete"),
        KeyboardButton(text="/help")
    )
    
    return builder.as_markup(resize_keyboard=True)

def deadline_keyboard():
    builder = ReplyKeyboardBuilder()
    
    builder.add(
        KeyboardButton(text="Today 🕒"),
        KeyboardButton(text="Tomorrow 📅"),
        KeyboardButton(text="Custom date 📆")
    )
    builder.adjust(2, 1)
    
    return builder.as_markup(resize_keyboard=True)

def back_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="↩️ Back"))
    
    return builder.as_markup(resize_keyboard=True)