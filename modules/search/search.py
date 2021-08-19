from bs4 import BeautifulSoup
import requests
import telebot
from fake_useragent import UserAgent
from loguru import logger

logger.add('../../logging/debug.txt', format="{time} {level} {message}", level="DEBUG") 
ua = UserAgent()

def search(text):
    headers = {
        "User-Agent": ua.random
    }
    logger.info(headers)
    link = "https://google.com/search?q={0}".format(text)
    req = requests.get(link, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")

    results = []
    for g in soup.find_all('div'):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            if link.startswith("/"):
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

    # print(results)

    text = "<a href='{0}'>[Search]</a>\n\n\n".format(req.url)
    steps = 0
    for i in results:
        tempText = "<a href='{0}'>{1}</a>\n\n".format(i['link'], i['title'])
        text += tempText
        steps += 1
        # if steps >= 10:
        #     break
    return text