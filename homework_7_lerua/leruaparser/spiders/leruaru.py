import scrapy
from scrapy.http import HtmlResponse

from homework_7_lerua.leruaparser.items import LeruaparserItem
from scrapy.loader import ItemLoader

class LeruaruSpider(scrapy.Spider):
    name = 'leruaru'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru']

    def __init__(self, search):
        super().__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search["query"]}']

    def parse(self, response:HtmlResponse):
        items = response.css("a.plp-item__info__title::attr(href)").extract()
        next = response.css("a.next-paginator-button::attr(href)").extract_first()
        for item in items:
            yield response.follow(item, callback=self.parse_item_async)

        if next:
            yield response.follow(next, callback=self.parse)

    #асинхронные парсинг с помощью ItemLoader
    def parse_item_async(self,response:HtmlResponse):
        loader = ItemLoader(item=LeruaparserItem(),response=response)
        loader.add_xpath('name',"//h1/text()")
        loader.add_css('price',"span[slot='price']::text")
        loader.add_css('currency',"span[slot='currency']::text")
        loader.add_css("param_keys", "div.def-list__group dt.def-list__term::text")
        loader.add_css("param_values", "div.def-list__group dd.def-list__definition::text")
        loader.add_xpath("photos","//uc-pdp-media-carousel//img[@slot='thumbs']/@src")

        loader.add_value('url',response.url)
        yield loader.load_item()
