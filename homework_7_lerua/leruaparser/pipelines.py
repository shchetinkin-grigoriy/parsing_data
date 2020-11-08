import hashlib

import scrapy
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes
from homework_7_lerua.leruaparser.items import LeruaparserItem


class LeruaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        db = client.leruadb
        self.products = db.products

    def process_item(self, item:LeruaparserItem, spider):
        item["params"] = dict()
        for key in range(len(item["param_keys"])):
            item["params"][item["param_keys"][key]] = item["param_values"][key]
        del item["param_keys"]
        del item["param_values"]
        self.products.update_one({'url' : item["url"]}, {'$set' : item}, upsert=True)
        return item

class LeruaparserPhoptosPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    request = scrapy.Request(url=img)
                    request.meta['name'] = item['name'].replace(" ", "_")
                    yield request
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]

        return item

    def file_path(self, request, response=None, info=None):
        product_name = request.meta['name']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        path = 'full/%s/%s.jpg' % (product_name, image_guid)
        return path
