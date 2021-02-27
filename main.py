# https://habr.com/ru/all/

import requests
from bs4 import BeautifulSoup
from pprint import pprint


KEYWORDS = ['дизайн', 'фото', 'web', 'python']

url = 'https://habr.com/ru/all/'
# Получим html
resp = requests.get(url)
resp.raise_for_status()
text = resp.text
# Подключим BS и найдем все посты
soup = BeautifulSoup(text, features="html.parser" )
articles = soup.findAll('article', class_='post')
# В каждом посте произведем проверку на равенство любого ключевого слова и тэга. При совпадении - записываем дату, заголовок и ссылку на пост.
for index, i in enumerate(articles):
    hub = i.findAll('a', class_='hub-link')
    hubs = [x for x in hub]
    let = False
    for hub in hubs:
        if any(KEY == hub.text.lower().strip() for KEY in KEYWORDS):
            let = True
    if let:
        date = i.find('span', class_='post__time').text 
        title = i.find('h2', class_='post__title').text
        post_url = i.find('a', class_='post__title_link').get('href')
        # Получим текст страницы поста и найдем там текст саомй статьи
        resp = requests.get(post_url)
        resp.raise_for_status()
        post_text_resp = resp.text

        soup_post = BeautifulSoup(post_text_resp, features="html.parser")
        post_text = soup_post.find('div', class_='post__body_full').text
        # Выведем полученные данные
        pprint({
            f'{index} пост' :{
                            'date': date.strip(),
                            'title': title.strip(),
                            'post_url': post_url.strip(),
                            'post_text': post_text.strip()
                             }
        })
        print()