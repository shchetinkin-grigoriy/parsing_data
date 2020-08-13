# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongo_base = client.vacansy


    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        # if spider.name == 'hhru':
        #     pass
        # else:
        #     pass
        # salary = item['item_salary']
        # item['min_salary'],item['max_salary'],item['cur'] = self.process_salary(salary)

        collection.insert_one(item)

        return item

    def process_salary(self, salary):

        min_salary,max_salary,cur = None,None,None
        return min_salary,max_salary,cur