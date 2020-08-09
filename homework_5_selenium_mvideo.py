# 2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД. Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары

# импорт классов
import time
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('start-maximized')

from datetime import date, timedelta

# 1. ИНИЦИАЛИЗАЦИЯ
driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
driver.get('https://www.mvideo.ru/')
print(driver.title)
assert "No results found." not in driver.page_source

# 2. ПОИСК ЭЛЕМЕНТА ПО ТЕКСТУ
time.sleep(3)
all_carousels = driver.find_elements_by_xpath("//div[contains(@data-init,'ajax-category-carousel')]")
hits_containers = list(
    filter(lambda x: 'Хиты продаж' in x.find_element_by_xpath(".//div[contains(@class,'gallery-title-wrapper')]").text,
           all_carousels))

assert len(hits_containers) == 1
container = hits_containers[0]
actions = ActionChains(driver)
actions.move_to_element(container)
actions.perform()

result_items = []
product_urls = set()
last_len = 0
# 2. ПЕРЕБОР ЭЛЕМЕНТОВ В КОНТЕЙНЕРЕ
while True:
    products = container.find_elements_by_xpath('.//li')

    for product in products:
        item_url = product.find_element_by_xpath(".//a[@class='sel-product-tile-title']").get_attribute("href")
        if not item_url in product_urls:
            product_urls.add(item_url)
            item = {}
            item['url'] = item_url
            item['name'] = product.find_element_by_xpath(".//h4").text
            item['price'] = product.find_element_by_xpath(
                ".//div[contains(@class, 'c-pdp-price__current')]").text.replace('\xa0', '')

            result_items.append(item)

    #ссылка на кнопку
    next_button = container.find_elements_by_class_name("next-btn")
    if last_len == len(product_urls) or not len(next_button):
        break

    last_len = len(product_urls)
    next_button[0].click()
    time.sleep(1)

pprint(result_items)
driver.close()

# 3 СЛОЖИТЬ ВСЕ В БД
from pymongo import MongoClient
client = MongoClient('127.0.0.1', 27017)
db = client['mvideo_db']
mvideo_db = db.mvideo

for item in result_items:
     mvideo_db.update_one({'link': item['url']}, {'$set': item}, upsert=True)

