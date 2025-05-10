# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SteamscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class HardwareItem(scrapy.Item):
    hardware_type = scrapy.Field()
    rank = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    timestamp = scrapy.Field()
