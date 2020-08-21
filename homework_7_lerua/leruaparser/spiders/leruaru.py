import scrapy


class LeruaruSpider(scrapy.Spider):
    name = 'leruaru'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['http://leroymerlin.ru/']

    def parse(self, response):
        pass
