from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from homework_7_lerua.leruaparser import settings

from homework_7_lerua.leruaparser.spiders.leruaru import LeruaruSpider

if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    search = {'query': 'стеллаж'}
    process = CrawlerProcess(settings=crawler_settings)

    process.crawl(LeruaruSpider, search=search)
    process.start()