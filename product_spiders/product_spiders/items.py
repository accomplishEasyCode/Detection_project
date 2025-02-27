# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# class TaobaoItem(scrapy.Item):
#     input=scrapy.Field()
#     id= scrapy.Field()
#     link = scrapy.Field()
#     merchants=scrapy.Field()
#     title=scrapy.Field()
#     platform=scrapy.Field()
#     product_category=scrapy.Field()
#     Authorization=scrapy.Field()
#
# class JingdongItem(scrapy.Item):
#     input=scrapy.Field()
#     id = scrapy.Field()
#     link = scrapy.Field()
#     merchants=scrapy.Field()
#     title=scrapy.Field()
#     platform=scrapy.Field()
#     product_category=scrapy.Field()
#     Authorization=scrapy.Field()

class TaobaoItem(scrapy.Item):
    input = scrapy.Field()
    id = scrapy.Field()
    link = scrapy.Field()
    merchants = scrapy.Field()
    title = scrapy.Field()
    platform = scrapy.Field()
    product_category = scrapy.Field()
    Authorization = scrapy.Field()
    price = scrapy.Field()  # 新增字段

class JingdongItem(scrapy.Item):
    input = scrapy.Field()
    id = scrapy.Field()
    link = scrapy.Field()
    merchants = scrapy.Field()
    title = scrapy.Field()
    platform = scrapy.Field()
    product_category = scrapy.Field()
    Authorization = scrapy.Field()
    price = scrapy.Field()  # 新增字段
import scrapy


