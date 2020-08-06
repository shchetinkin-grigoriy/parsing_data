#1)Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex.ru/news
#Для парсинга использовать xpath. Структура данных должна содержать:
#* название источника,
#* наименование новости,
#* ссылку на новость,
#* дата публикации

from homework_4_lenta import get_news_by_lenta
from homework_4_mail import get_news_by_mail
from homework_4_yandex import get_news_by_yandex
from pymongo import MongoClient
from pprint import pprint

news = []
news += get_news_by_mail()
news += get_news_by_lenta()
news += get_news_by_yandex()

pprint(news)

#2)Сложить все новости в БД

client = MongoClient('127.0.0.1', 27017)
db = client['news_db']
news_db = db.news

for new in news:
    news_db.update_one({'link': new['link']}, {'$set': new}, upsert=True)

