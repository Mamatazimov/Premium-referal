import logging
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.filters import CommandStart
from config import Bot_Token, Admin_Id
from handlers import register_handlers
from database.db import init_db



dp = Dispatcher()
bot = Bot(Bot_Token,default=DefaultBotProperties(parse_mode=ParseMode.HTML))
init_db()
register_handlers(dp)








if __name__ == "__main__":
    dp.run_polling(bot, skip_updates=True)


