# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from homework_6.jobscraper.items import JobscraperItem
from pymongo import MongoClient
import re

class JobscraperPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        db = client['homework_6_db']
        self.vacancies = db.vacancies

    def process_item(self, item:JobscraperItem, spider):
        if spider.name == 'hhru':
            salary_text = list(map(str.strip, item["salary_text"]))
            item["salary_min"] = self.get_salary_min_hh(salary_text)
            item["salary_max"] = self.get_salary_max_hh(salary_text)
            item["salary_cur"] = salary_text[-2] if item["salary_min"] or item["salary_max"] else None
            item["salary_text"] = None
        elif spider.name == 'superjobru':
            salary_text = list(map(str.strip, item["salary_text"]))
            item["salary_min"], item["salary_max"], item["salary_cur"] = self.get_salary_superjob(salary_text)
            item["salary_text"] = None

        self.vacancies.update_one({'url' : item["url"]}, {'$set' : item}, upsert=True)

        return item

    def get_salary_min_hh(self, salary_text:list):
        if salary_text:
            if 'от' in salary_text:
                index = salary_text.index('от')
                return salary_text[index+1].replace('\xa0', '')
            elif '-' in salary_text:
                index = salary_text.index('-')
                return salary_text[index - 1].replace('\xa0', '')
            elif 'до' not in salary_text:
                for item in salary_text:
                    item:str = item.replace('\xa0', '')
                    if item.isnumeric():
                        return int(item)

        return None

    def get_salary_max_hh(self, salary_text:list):
        if salary_text:
            if 'до' in salary_text:
                index = salary_text.index('до')
                return salary_text[index+1].replace('\xa0', '')
            elif '-' in salary_text:
                index = salary_text.index('-')
                return salary_text[index + 1].replace('\xa0', '')
            elif 'от' not in salary_text:
                for item in salary_text:
                    item:str = item.replace('\xa0', '')
                    if item.isnumeric():
                        return int(item)

        return None

    def get_salary_superjob(self, salary_text:list):
        salary_min = None
        salary_max = None
        salary_cur = None
        if salary_text:
            if 'от' in salary_text:
                index = salary_text.index('от')
                text = salary_text[index + 2].replace('\xa0', '')
                salary_min = int(re.sub('[^\d]', '', text))
                salary_cur = re.sub('\d', '', text)
            elif 'до' in salary_text:
                    index = salary_text.index('до')
                    text = salary_text[index + 2].replace('\xa0', '')
                    salary_max = int(re.sub('[^\d]', '', text))
                    salary_cur = re.sub('\d', '', text)
            elif 'до' not in salary_text and 'от' not in salary_text:
                for item in salary_text:
                    item:str = item.replace('\xa0', '')
                    if item.isnumeric():
                        salary_min = int(item)
                        break
                for item in salary_text[::-1]:
                    item:str = item.replace('\xa0', '')
                    if item.isnumeric():
                        salary_max = int(item)
                        break
                salary_cur = salary_text[-1]

        return salary_min, salary_max, salary_cur
