# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Ira1Item(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    body = scrapy.Field()
    pageid = scrapy.Field()
    url = scrapy.Field()
    mails = scrapy.Field()
    
