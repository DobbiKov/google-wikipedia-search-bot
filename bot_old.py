import telebot
from telebot import types
from modules.search.search import search
from modules.wikipedia import wikipediaSearch
from mtranslate import translate
from data.config import TOKEN
bot = telebot.TeleBot(TOKEN)

searches = []
wikipediaSearches = []

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Привет! Я телеграм бот для поиска в гугл.\n\nКак мной пользоваться:\nОтправляешь мне текст и бот тебе выдает ответы.")

@bot.message_handler(content_types=['text'])
def send_text(message: types.Message):
    if(message.text == "/start"):
        return

    objToList = {'user_id': message.from_user.id, 'text': message.text}
    searches.append(objToList)
    markup3 = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("Google", callback_data="dobbikov_google")
    item2 = types.InlineKeyboardButton("Wikipedia", callback_data="dobbikov_wikipedia")
    item3 = types.InlineKeyboardButton("Перевести на русский", callback_data="dobbi_trans_ru")
    item4 = types.InlineKeyboardButton("Перевести на английский", callback_data="dobbi_trans_en")

    markup3.add(item1, item2)
    markup3.add(item3)
    markup3.add(item4)
    bot.send_message(message.chat.id, "Ищем в гугле, или википедии?", reply_markup=markup3)

def getSearchesText(userId):
    text = "DOBBIKOV_ERROR"
    for i in searches:
        if i['user_id'] == userId:
            print("tut!") #
            text = i['text']
            searches.pop(searches.index(i))
            break
    return text

def botGoogleSearch(userId):
    text = "DOBBIKOV_ERROR"
    text = getSearchesText(userId)
    if(text != "DOBBIKOV_ERROR"):
        text = search(text)
    else:
        text = "ERROR!"
    # print(text)
    bot.send_message(userId, text, parse_mode='html')

def botWikipediaSearch(userId):
    text = "DOBBIKOV_ERROR"
    text = getSearchesText(userId)

    markup3 = types.InlineKeyboardMarkup()
    if(text != "DOBBIKOV_ERROR"):
        arr = wikipediaSearch.search("ru", text)
        if arr[0] == []:
            text = "Вариантов ответа по вашему запросу не найдено!"
        else:
            text = "Варианты ответа по вашему запросу:"
            objToList = {'user_id': userId, 'searches': arr[0]}
            wikipediaSearches.append(objToList)
            steps = 0
            for i in arr[0]:
                if i == "":
                    continue
                try:
                    button = types.InlineKeyboardButton(i, callback_data="d_wiki_s_{0}".format(arr[0].index(i)))
                except:
                    continue
                steps += 1
                markup3.add(button)

    else:
        text = "ERROR!"
    # print(text)
    bot.send_message(userId, text, parse_mode='html', reply_markup=markup3)

def botWikipediaArticle(userId, text):

    ourSearch = ""
    for i in wikipediaSearches:
        if i['user_id'] == userId:
            ourSearch = i['searches'][int(text)]
    
    if ourSearch == None or ourSearch == "":
        bot.send_message(userId, "Возникла техническая ошибка. Приносим свои извинения.", parse_mode='html')
        return

    article = "{0}\n\n".format(ourSearch)
    tempArticle = wikipediaSearch.article("ru", ourSearch)
    if tempArticle == None or tempArticle == "":
        bot.send_message(userId, "Возникла ошибка на стороне Википедии. Приносим свои извинения.", parse_mode='html')
        return
    article += tempArticle

    markup3 = types.InlineKeyboardMarkup()
    link = wikipediaSearch.link("ru", ourSearch)
    if link != "" and link != None:
        button = types.InlineKeyboardButton("Ссылка", url=link)
        markup3.add(button)
    bot.send_message(userId, article, parse_mode='html', reply_markup=markup3)

def botTranslate(userId, lang):
    text = getSearchesText(userId)

    transTextToBot = "Ваш перевод:\n\n"
    transText = translate(text, lang, "auto")
    transTextToBot += transText

    bot.send_message(userId, transTextToBot, parse_mode='html')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global bot
    if call.message:
        if call.data == 'dobbikov_google':
            botGoogleSearch(call.message.chat.id)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Ищем в гугле, или википедии?", reply_markup=None)  
        elif call.data == 'dobbikov_wikipedia':
            print("TUT2")
            botWikipediaSearch(call.message.chat.id)
            print("TUT3")
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Ищем в гугле, или википедии?", reply_markup=None) 
        elif call.data.startswith("d_wiki_s_"):
            botWikipediaArticle(call.message.chat.id, call.data.replace("d_wiki_s_", ""))
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        elif call.data.startswith('dobbi_trans_'):
            botTranslate(call.message.chat.id, call.data.replace("dobbi_trans_", ""))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Ищем в гугле, или википедии?", reply_markup=None) 
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Ищем в гугле, или википедии?", reply_markup=None) 

            # показать оповещение
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
        text="Преобразовано...")

bot.polling()


