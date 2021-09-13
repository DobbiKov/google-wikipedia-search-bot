from utils.on_startup_notify import on_startup_notify
from modules.search.search import search
from modules.wikipedia import wikipediaSearch
from mtranslate import translate
from data.config import TOKEN
import logging

from aiogram import Bot, Dispatcher, executor, types
from handlers import dp
from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    await on_startup_notify(dp)
    await set_default_commands(dp)

    print("~~~~~ Bot was started ~~~~~")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)