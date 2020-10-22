import re
import warnings
import pandas as pd
import scrapy


START_URL = r"https://www.lgcstandards-atcc.org/search#sort=relevancy&f:contentTypeFacetATCC=[Products]&f:productcategoryFacet=[Cell%20Lines%20%26%20Hybridomas]"


class ATCCSpider(scrapy.Spider):
    name = "ATCC"

    def start_requests(self):
        
        raise NotImplementedError("Doesn't work")

        self.settings['ROBOTSTXT_OBEY'] = False
        obey_robotstxt = self.settings['ROBOTSTXT_OBEY']
        if not obey_robotstxt:
            warnings.warn('ATCC bot not obeying robots.txt')

        urls = [START_URL]
        for url in urls:
            yield scrapy.Request(
                url=url, 
                callback=self.parse_catalog_page
            )

    def parse_catalog_page(self, response):
        
        # Get links to cell lines from current catalog page
        celllines_links = self.get_celllines_links(response)
        yield from response.follow_all(
            celllines_links,
            self.parse_cellline_page
        )

        # Get link to next page
        next_page_link = self.get_next_page(response)
        assert len(next_page_link) == 1
        yield from response.follow_all(
            next_page_link,
            self.parse_catalog_page
        )

    def get_celllines_links(self, response):
        raise NotImplementedError

    def get_next_page(self, response):
        raise NotImplementedError

    def parse_cellline_page(self, response):
        raise NotImplementedError