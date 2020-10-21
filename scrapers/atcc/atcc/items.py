# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AtccItem(scrapy.Item):
    # An ATCC cellline
    name = Field()
    organism = Field()
    celltype = Field()
    disease = Field()