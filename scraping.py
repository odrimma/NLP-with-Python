from bs4 import BeautifulSoup
from urllib.parse import quote_plus

from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError

def error_processing(url):
   try:
      html = urlopen(url)
   except HTTPError as e:
      print('На сервере нет такой страницы!')
      return None
   except URLError as e:
      print('Сервер не найден!')
      return None
   return html

def scraping(url, name):
   data_list = []
   # Проходимся с 1 по 50 страницу
   for item in range(1, 51):
      html = error_processing(url + 'page{}/?q={}&target_type=posts&order=relevance'.format(item, quote_plus(name)))
      if html:
         bs = BeautifulSoup(html.read(), 'html.parser')
         # Находим всех родителей, т.е. блоки со статьями
         perents = bs.find_all('article', {'class': 'tm-articles-list__item'})
         # Проходим по всем родителям и получаем нужную нам информацию: автор статьи, название публикации, ссылка на статью и тэги статьи
         for perent in perents:
            autor = perent.find('span', {'class': 'tm-user-info tm-article-snippet__author'})
            pub_name = perent.find('h2', {'class': 'tm-article-snippet__title tm-article-snippet__title_h2'})
            pub_text = perent.find('div', {'class': {'article-formatted-body article-formatted-body_version-2', 'article-formatted-body article-formatted-body_version-1'}})
            Href = perent.find('a', {'class': 'tm-article-snippet__title-link'})
            tegs = perent.find_all('a', {'class': 'tm-article-snippet__hubs-item-link'})
            tegs_list = []
            for teg in tegs:
               tegs_list.append('https://habr.com' + str(teg.attrs['href']).strip())
            data_list.append({
               'Автор': str(autor.text.strip()) if autor else '',
               'Название': str(pub_name.text.strip()) if pub_name else '',
               'Превью': str(pub_text.text.strip()) if pub_text else '',
               'Ссылка': 'https://habr.com' + str(Href.attrs['href'].strip()) if Href else '',
               'Тэги': tegs_list if tegs_list else ' '
            })
         print('Страница ' + f'{item}: Готов')
   return data_list

