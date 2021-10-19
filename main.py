from scraping import scraping
from nlp import *
from in_out_json import *

from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def main_nlp(data):
    total_pub = 1
    total_persons = []
    c = Counter()
    for item in data:
        names, tokens = nlp_fun(item['Превью'])
        if tokens:
            for jtem in tokens:
                if jtem.pos == ('NOUN' or 'ADJF' or 'VERB' or 'ADVB'):
                    c[jtem.lemma] += 1
        total_persons += names
        print('Статья {} - Готов'.format(total_pub))
        if total_pub > 200:
            total_persons = [key for key, value in Counter(total_persons).most_common(15)]
            for key, value in list(c.items()):
                if value < 20:
                    del c[key]
            total_terms = list(c.elements())
            total_persons = list(set(total_persons))
            return total_terms, total_persons
        total_pub += 1
def create_cloud(total_terms, filename):
    try:
        print("Создаем облако тегов...")
        cloud = WordCloud(width=2000, height=1500, random_state=1, background_color='black', margin=20, colormap='Pastel1', collocations=False,).generate(' '.join(total_terms))
        cloud.to_file(filename + '.png')
    except:
        print('Не удалось создать облако тэгов!')
        return

def main():
    print('Извлекаем информацию из источников...')
    data_list = scraping('https://habr.com/ru/search/', 'криптография')
    if not writing_json(data_list, 'data.json'):
        return None
    print('Извлечение завершено!')
    data = read_json('data.json')
    if not data:
        return None
    print('Поиск ключевых персонажей и терминов...')
    total_terms, names = main_nlp(data)
    writing_json(names, 'KeyPerson.json')
    create_cloud(total_terms, 'TermCloud')
    print('Готово!')

main()
