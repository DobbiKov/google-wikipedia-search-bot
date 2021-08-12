import wikipedia

def search(lang, text):
    wikipedia.set_lang(lang)
    return wikipedia.search(text, suggestion=True)

def article(lang, title):
    wikipedia.set_lang(lang)
    for _ in range(3):
        try:
            summary = wikipedia.summary(title, sentences=6)
            return summary
        except wikipedia.exceptions.DisambiguationError as exc:
            title = exc.options[0]
        except wikipedia.exceptions.PageError:
            return
def link(lang, title):
    wikipedia.set_lang(lang)
    try:
        page = wikipedia.page(title)
        path = page.title.replace(' ', '_')
        return f'https://{lang}.wikipedia.org/wiki/{path}'
    except Exception:
        print('Error while making link')
