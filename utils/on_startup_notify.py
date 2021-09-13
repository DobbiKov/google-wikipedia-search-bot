import asyncio
from aiogram import Dispatcher

from data.config import ADMINS
from loader import bot
from utils.send_all_admin import send_all_admin

async def on_startup_notify(dp: Dispatcher):
        await send_all_admin(dp, f"<b>Бот был успешно запущен</b>\n")