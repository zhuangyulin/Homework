# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GujiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    booktitle = scrapy.Field()
    bookhref = scrapy.Field()
    brief = scrapy.Field()
    messagetitle = scrapy.Field()
    messagehref = scrapy.Field()
    messagebrief = scrapy.Field()
