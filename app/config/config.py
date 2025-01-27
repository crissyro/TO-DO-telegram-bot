import os
import logging
from aiogram import Bot

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)

class Config:
    logger = logging.getLogger(__name__)
    bot = Bot(token=os.getenv('BOT_TOKEN'))

