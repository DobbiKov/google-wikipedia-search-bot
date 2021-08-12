import mwclient

site = mwclient.Site('ru.wikipedia.org')
page = site.pages[u'Автомобиль']
print(page.text())