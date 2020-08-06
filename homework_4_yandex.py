import requests
from lxml import html
from pprint import pprint

from pymongo import MongoClient

from datetime import date


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
#функция получения ин-формации с yandex.ru
def get_news_by_yandex():
    #инициализация
    url = 'https://yandex.ru/news/'
    response = requests.get(url, headers)
    dom = html.fromstring(response.text)

    result = []

    items = dom.xpath("//article")
    for item in items:
        new = {}
        new['link'] = url + item.xpath(".//a[contains(@class,'news-card__link')]/@href")[0]
        new['name'] = item.xpath(".//h2[contains(@class,'news-card__title')]/text()")[0].replace('\xa0',' ')
        new['source'] = item.xpath(".//span[contains(@class,'mg-card-source__source')]/a/text()")[0]
        time = item.xpath(".//span[contains(@class,'mg-card-source__time')]/text()")[0]
        new['date'] = f'{date.today()} {time}'

        result.append(new)

    return result


if __name__ == '__main__':
    pprint(get_news_by_yandex())
