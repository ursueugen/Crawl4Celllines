from pathlib import Path
from selenium.webdriver import Firefox

FIREFOX_DRIVER_PATH = Path("../../bin/geckodriver")
ATCC_CELLLINES_PRIMARY_STEM_PRODUCTS_CATALOG_URL = r"https://www.lgcstandards-atcc.org/search#sort=relevancy&f:contentTypeFacetATCC=[Products]&f:productcategoryFacet=[Cell%20Lines%20%26%20Hybridomas,Primary%20Cells,Stem%20Cells]" 

def build_browser(
    start_url: str = ATCC_CELLLINES_PRIMARY_STEM_PRODUCTS_CATALOG_URL,
    driver_path: Path = FIREFOX_DRIVER_PATH
    ) -> Firefox:
    
    raise NotImplementedError('Add VPN, check Firefox settings on limiting the bot')
    browser = Firefox(executable_path=driver_path, headless=True)
    browser.headless = True
    browser.get(start_url)
    return browser

def find_celllines_links(browser):
    cellines_links_xpath = '//a[starts-with(@href, "/products")]'
    elems = (
        browser
        .find_elements_by_xpath(
            cellines_links_xpath
        )
    )
    links_to_celllines_pages = set(
        map(
            lambda e: e.getAttribute("href"),
            elems
        )
    )
    return links_to_celllines_pages

# elem.tag_name
# elem.get_attribute('href')
# set(links)

if __name__ == '__main__':
    browser = build_browser()
