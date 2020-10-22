from pathlib import Path
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.webelement import FirefoxWebElement
import typing


FIREFOX_DRIVER_PATH = Path("../../bin/geckodriver")
ATCC_CELLLINES_PRIMARY_STEM_PRODUCTS_CATALOG_URL = r"https://www.lgcstandards-atcc.org/search#sort=relevancy&f:contentTypeFacetATCC=[Products]&f:productcategoryFacet=[Cell%20Lines%20%26%20Hybridomas,Primary%20Cells,Stem%20Cells]" 
LIMIT_CATALOG_PAGES = 1


def build_browser(
    start_url: str,
    driver_path: Path,
    force_exec = False
    ) -> Firefox:
    
    if not force_exec:
        raise NotImplementedError('Add VPN, check Firefox settings on limiting the bot')
    
    browser = Firefox(executable_path=driver_path)
    browser.headless = True
    browser.get(start_url)
    return browser

def find_celllines_links(browser: Firefox) -> list:
    cellines_links_xpath = '//a[starts-with(@href, "/products")]'
    elems = (
        browser
        .find_elements_by_xpath(
            cellines_links_xpath
        )
    )
    links_to_celllines_pages = set(
        map(
            lambda e: e.get_attribute("href"),
            elems
        )
    )
    return links_to_celllines_pages

def find_next_page(
    browser: Firefox
    ) -> FirefoxWebElement or None:
    
    next_page_button_xpath = '//a[@title="Next"]'
    button = browser.find_elements_by_xpath(
        next_page_button_xpath
    )

    assert len(button) <= 1, "find_next_page: Got >1 next page buttons."
    if len(button) == 0:
        return None
    else:
        return button[0]

def go_next_page(browser: Firefox) -> bool:
    next_page_button = find_next_page(browser)

    if next_page_button:
        # browser goes to next page
        next_page_button.click()
        return True
    return False

def crawl(browser: Firefox, limit: int or None = None):
    catalog_page_counter = 0
    while go_next_page(browser):
        celllines_links = find_celllines_links(browser)
        extract_celllines(celllines_links)
        
        # Break at limit if set up.
        catalog_page_counter += 1
        reached_limit = (
            limit is not None 
            and catalog_page_counter == limit
        )
        if reached_limit:
            break

def extract_celllines(cellline_links):
    raise NotImplementedError

if __name__ == '__main__':
    browser = build_browser(
        start_url=ATCC_CELLLINES_PRIMARY_STEM_PRODUCTS_CATALOG_URL,
        driver_path=FIREFOX_DRIVER_PATH
    )

    crawl(
        browser,
        limit=LIMIT_CATALOG_PAGES
    )