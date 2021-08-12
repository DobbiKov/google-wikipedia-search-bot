from bs4 import BeautifulSoup
import requests
import telebot
from config import TOKEN
from config import BOT_OWNER

bot = telebot.TeleBot(TOKEN)


link = "https://google.com/search?q={0}".format("торгабалин")

req = requests.get(link)

soup = BeautifulSoup(req.text, "html.parser")

results = []
for g in soup.find_all('div'):
    anchors = g.find_all('a')
    if anchors:
        link = anchors[0]['href']
        if link.startswith("/url"):
            link = "https://google.com" + link
        try:
            title = g.find('h3').text
        except:
            continue
        item = {
            "title": title,
            "link": link
        }
        results.append(item)

print(results)

text = "<a href='{0}'>[Search]</a>\n\n".format(req.url)
steps = 0
for i in results:
    tempText = "<a href='{0}'>{1}</a>\n".format(i['link'], i['title'])
    text += tempText
    steps += 1
    # if steps >= 10:
    #     break

bot.send_message(BOT_OWNER, text, parse_mode='html')