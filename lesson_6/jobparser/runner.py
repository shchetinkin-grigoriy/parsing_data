from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lesson_6.jobparser import settings
from lesson_6.jobparser.spiders.hhru import HhruSpider
# from jobparser.spiders.sjru import SjruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    # process.crawl(SjruSpider)
    process.crawl(HhruSpider)
    process.start()