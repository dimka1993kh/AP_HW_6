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
    # Найдем полный текст статьи
    post_url = i.find('a', class_='post__title_link').get('href')
    resp = requests.get(post_url)
    resp.raise_for_status()
    post_text_resp = resp.text
    soup_post = BeautifulSoup(post_text_resp, features="html.parser")
    post_text = soup_post.find('div', class_='post__body_full').text.lower().strip().split()
    # Найдеи тэги, превью, заголовок
    hub = i.findAll('a', class_='hub-link')
    preview = i.find('div', class_='post__text').text.lower().strip().split()
    title = i.find('a', class_='post__title_link').text.lower().strip().split()

    hubs = [x.text.lower().strip().split() for x in hub] + preview + title + post_text
    let = False
    for hub in hubs:
        for key in KEYWORDS:
            if key == hub:
                let = True
                # print(key)
    if let:
        date = i.find('span', class_='post__time').text 
        title = i.find('h2', class_='post__title').text
        post_url = i.find('a', class_='post__title_link').get('href')
        
        # Выведем полученные данные
        pprint({
            f'{index + 1} пост' :{
                            'date': date.strip(),
                            'title': title.strip(),
                            'post_url': post_url.strip(),
                            # 'post_text': post_text.strip()
                             }
        })
        print()