import requests
from lxml import html
from pprint import pprint

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}


# функция получения ин-формации с mail.ru
def get_news_by_mail():
    # инициализация
    url = 'https://news.mail.ru'
    response = requests.get(url, headers)
    dom = html.fromstring(response.text)

    result = []
    # основной блок новостей - с картинками
    items = dom.xpath("//table[@class='daynews__inner']//div[contains(@class,'daynews__item')]")
    for item in items:
        new = {}
        new['link'] = url + item.xpath("./a[@href]/@href")[0]
        new['name'] = item.xpath("./a[@href]//span[contains(@class,'photo__title')]/text()")[0].replace('\xa0', ' ')

        # подзапрос на страницу
        response_inner = requests.get(new['link'], headers)
        dom_inner = html.fromstring(response_inner.text)
        breadcrumbs_bar = dom_inner.xpath("//div[contains(@class, 'breadcrumbs')]")[0]

        new['source'] = breadcrumbs_bar.xpath(".//a[contains(@class, 'breadcrumbs__link')]/span/text()")[0]
        new['date'] = breadcrumbs_bar.xpath(".//span[@datetime]/@datetime")[0]
        result.append(new)

    # блок новостей политики
    items = dom.xpath(
        "//div[@class='wrapper js-module']//a[@href='/politics/']/ancestor::div[contains(@class, 'cols__inner')]//a[contains(@class, 'link')]")
    for item in items:
        new = {}

        new['link'] = item.xpath("./@href")[0]

        # подзапрос на страницу
        response_inner = requests.get(new['link'], headers)
        dom_inner = html.fromstring(response_inner.text)

        # Тут проще имя брать с самой страницы новости
        new['name'] = dom_inner.xpath("//div[contains(@class, 'meta-speakable-title')]//h1/text()")[0].replace('\xa0',
                                                                                                               ' ')

        breadcrumbs_bar = dom_inner.xpath("//div[contains(@class, 'breadcrumbs')]")[0]
        new['source'] = breadcrumbs_bar.xpath(".//a[contains(@class, 'breadcrumbs__link')]/span/text()")[0]
        new['date'] = breadcrumbs_bar.xpath(".//span[@datetime]/@datetime")[0]
        result.append(new)

    return result


if __name__ == '__main__':
    pprint(get_news_by_mail())
