from pathlib import Path
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.webelement import FirefoxWebElement
import warnings
import time
import json


FIREFOX_DRIVER_PATH = Path("../../bin/geckodriver")
ATCC_CELLLINES_PRIMARY_STEM_PRODUCTS_CATALOG_URL = r"https://www.lgcstandards-atcc.org/search#sort=relevancy&f:contentTypeFacetATCC=[Products]&f:productcategoryFacet=[Cell%20Lines%20%26%20Hybridomas,Primary%20Cells,Stem%20Cells]" 
OUTPUT_PATH = Path("../../data/atcc/cellline_links.json")

FORCE_EXECUTION = True
LIMIT_CATALOG_PAGES = None
PAGE_LOAD_TIMEOUT = 1


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

def find_celllines_links(
    browser: Firefox,
    timeout: int = PAGE_LOAD_TIMEOUT) -> list:

    time.sleep(timeout)

    cellines_links_xpath = '//a[starts-with(@href, "/products")]'
    find_celllines = (
        lambda browser: (
            browser
            .find_elements_by_xpath(
                cellines_links_xpath
            )
        )
    )
    elems = find_celllines(browser)
    ### The snippet below doesn't work
    # elems = (
    #     WebDriverWait(
    #         browser,
    #         timeout=timeout
    #     ).until(
    #          find_celllines
    #     )
    # )
    
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

    if next_page_button is not None:
        # browser goes to next page
        next_page_button.click()
        return True
    return False

def crawl(browser: Firefox, limit: int or None = None):
    cellline_links = set()
    catalog_page_counter = 0
    while go_next_page(browser):
        links = find_celllines_links(browser)
        cellline_links = cellline_links.union(extract_celllines(links))
        
        # Break at limit if set up.
        catalog_page_counter += 1
        print(f"Browser location: Page {catalog_page_counter}")
        has_reached_limit = (
            limit is not None 
            and catalog_page_counter == limit
        )
        if has_reached_limit:
            end_crawl(browser, cellline_links)
            break
    else:
        end_crawl(browser, cellline_links)

def end_crawl(
    browser: Firefox,
    cellline_links: set,
    out_path: Path = OUTPUT_PATH):
    browser.close()
    write_to_json(list(cellline_links), out_path)

def write_to_json(s, path):
    with open(path, 'w+') as f:
        json.dump(s, f)

def extract_celllines(cellline_links):
    return cellline_links
    warnings.warn('Extraction not implemented')

if __name__ == '__main__':
    browser = build_browser(
        start_url=ATCC_CELLLINES_PRIMARY_STEM_PRODUCTS_CATALOG_URL,
        driver_path=FIREFOX_DRIVER_PATH,
        force_exec=FORCE_EXECUTION
    )

    crawl(
        browser,
        limit=LIMIT_CATALOG_PAGES
    )