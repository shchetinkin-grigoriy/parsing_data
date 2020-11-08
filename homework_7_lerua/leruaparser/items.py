
import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def process_params(value):
    return value.strip()

def process_price(value:str):
    return int(value.replace(" ", "").strip())


class LeruaparserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(process_price), output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())
    params = scrapy.Field()
    param_keys = scrapy.Field(input_processor=MapCompose(process_params))
    param_values = scrapy.Field(input_processor=MapCompose(process_params))
    photos = scrapy.Field()
    pass
