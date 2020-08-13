# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
import scrapy


class JobparserItem(scrapy.Item):
    _id = scrapy.Field()
    item_name = scrapy.Field()
    item_salary = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
