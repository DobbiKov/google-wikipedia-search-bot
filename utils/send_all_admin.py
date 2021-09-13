import asyncio
import logging
from aiogram import Dispatcher

from data.config import ADMINS
from loader import bot

async def send_all_admin(dp: Dispatcher, text: str):
    if(len(ADMINS) <= 0):
        logging.warn("You don't set admins of bot!")
        return
    
    for i in ADMINS:
        if type(i) != int:
            logging.warn("Id of someone your admin not number!")
            continue
        try:
            await bot.send_message(i, text)
        except Exception as ex:
            await logging.error("You set not your's admins id? or you not written to bot.")
