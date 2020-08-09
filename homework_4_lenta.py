import requests
from lxml import html
from pprint import pprint

from datetime import date


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
#функция получения ин-формации с Lenta.ru
def get_news_by_lenta():
    #инициализация
    url = 'https://lenta.ru'
    response = requests.get(url, headers)
    dom = html.fromstring(response.text)

    result = []
    #основной блок новостей - с картинками

    #items = dom.xpath("//div[@class='span4']//div[@class='titles']")
    #items = dom.xpath("//div[@class='span4']//div[@class='first-item']/h2")

    items = dom.xpath("//div[contains(@class, 'span4')]/div[@class='item'] | //div[contains(@class, 'span4')]//div[@class='first-item']/h2")
    for item in items:
        new = {}
        new['link'] = url + item.xpath("./a[@href]/@href")[0]
        new['name'] = item.xpath("./a[@href]/text()")[0].replace('\xa0',' ')
        new['source'] = 'Lenta.ru'
        new['date'] = item.xpath("./a[@href]/time/@datetime")[0]

        result.append(new)

    items = dom.xpath("//div[contains(@class, 'span4')]//div[contains(@class,'item news')]")
    for item in items:
        new = {}
        new['link'] = url + item.xpath(".//a[@href]/@href")[0]
        new['name'] = item.xpath(".//a[@href]/span/text()")[0].replace('\xa0',' ')
        new['source'] = 'Lenta.ru'
        time = item.xpath(".//span[contains(@class,'item__date')]/span[@class='time']/text()")[0]
        new['date'] = f'{date.today()} {time}'

        result.append(new)


    return result

if __name__ == '__main__':
    pprint(get_news_by_lenta())

