from utils.consts import CALLBACK_DATA_SEARCH_GOOGLE, CALLBACK_DATA_SEARCH_WIKIPEDIA, CALLBACK_DATA_TRANSLATE_EN, CALLBACK_DATA_TRANSLATE_RU
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_inline():
    keyboard = InlineKeyboardMarkup()
    
    item1 = InlineKeyboardButton("Google", callback_data=CALLBACK_DATA_SEARCH_GOOGLE)
    item2 = InlineKeyboardButton("Wikipedia", callback_data=CALLBACK_DATA_SEARCH_WIKIPEDIA)
    item3 = InlineKeyboardButton("Перевести на русский", callback_data=CALLBACK_DATA_TRANSLATE_RU)
    item4 = InlineKeyboardButton("Перевести на английский", callback_data=CALLBACK_DATA_TRANSLATE_EN)

    keyboard.add(item1, item2)
    keyboard.add(item3)
    keyboard.add(item4)
    return keyboard