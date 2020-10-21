import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


import re
import warnings
import pandas as pd


class ECACCSpider(scrapy.Spider):
    name = "ECACC"
    
    def start_requests(self):
        """
        Generates the starting URLs for scraping.
        Number of pages and base URL from ECACC is hard coded.
        """
        NUM_PAGES = 74
        warnings.warn('ECACCSpider: Num pages is hard-coded!')
        
        URL_TEMPLATE = "https://www.phe-culturecollections.org.uk/products/celllines/generalcell/browse.jsp?a2z=All&d-49653-p={}"
        urls = [URL_TEMPLATE.format(i) for i in range(1, NUM_PAGES+1)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_catalog_page)

    def parse_catalog_page(self, response):
        """
        Parses a page from the catalog of cell lines, typically 20 cell lines.
         Extracts URLs to cell lines' pages and queues them for scraping.
        """
        # Get all cell lines' ids from the current catalog page.
        xpath_pattern = r'//tbody//a//text()'
        extracts = response.xpath(xpath_pattern).getall()
        
        # Filter catalog numbers from extracted links.
        only_digits_regex = r"^[0-9]*$"
        catalog_nums = filter(lambda x: re.match(only_digits_regex, x), set(extracts))

        # Func to build URL to follow for cell lines' pages.
        URL_TEMPLATE = '/products/celllines/generalcell/detail.jsp?refId={}&collection=ecacc_gc'
        build_url = lambda catalog_num: response.urljoin(URL_TEMPLATE.format(catalog_num))
        
        # Build links to cell lines' pages and follow them.
        links_to_celllines = [build_url(catalog_num) for catalog_num in catalog_nums]
        yield from response.follow_all(links_to_celllines, self.parse_cellline_page)
    
    def parse_cellline_page(self, response):
        """
        Parses a cellline's page. Extracts relevant table and yields it as a dict record.
        """
        table_html = response.xpath('//table').get()
        df = pd.read_html(io=table_html)[0]
        record = df.dropna().set_index(0)[1].to_dict()
        record.update({'link': response.url})  # add link
        yield record