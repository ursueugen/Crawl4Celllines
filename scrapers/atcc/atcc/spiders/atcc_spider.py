import scrapy
from scrapy.selector import Selector

MOUSE_CELLLINES_URL = r'https://www.lgcstandards-atcc.org/search#sort=relevancy&f:contentTypeFacetATCC=[Products]&f:productcategoryFacet=[Cell%20Lines%20%26%20Hybridomas]&f:celloriginFacet=[Mouse]'

class ATCCSpider(scrapy.Spider):
    name = "ATCC"
    allowed_domains = ['lgcstandards-atcc.org']
    start_urls = [
        MOUSE_CELLLINES_URL,
    ]

    def parse(self, response):
        xpath_extract_celllines = r'//div/a[@class="coveo-title CoveoResultLink genomic-head"]/text()'
        celllines = Selector(response).xpath(xpath_extract_celllines).extract()
        print(response.url)
        print(celllines)