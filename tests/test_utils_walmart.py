from grocerygo_plus.grocerygo.web_crawler.utils_walmart import has_subcategory,click_next_page
import os
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
def test_has_subcategory():
    leaf_category = 'https://www.walmart.ca/en/grocery/meat-seafood/bacon/N-4526'
    root_category = 'https://www.walmart.ca/en/grocery/frozen-food/ice-cream-treats/N-3828'
    assert not has_subcategory(leaf_category, headless=False, disableimage=True)
    assert len(has_subcategory(root_category, headless=False, disableimage=True)) == 6


def test_click_next_page():
    web_driver_loc = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'chromedriver.exe')
    no_nextpage = 'https://www.walmart.ca/en/grocery/N-117+34081'
    has_nextpage = 'https://www.walmart.ca/en/grocery/pantry-food/chips-snacks/fruit-snacks/N-3782'
    last_pageofnextpage = 'https://www.walmart.ca/en/grocery/pantry-food/chips-snacks/fruit-snacks/N-3782/page-2'
    options = Options()
    options.add_argument('--blink-settings=imagesEnabled=false')
    driver = webdriver.Chrome(web_driver_loc, options=options)
    driver.get(has_nextpage)
    assert click_next_page(driver)
    driver.get(last_pageofnextpage)
    assert not click_next_page(driver)
    driver.get(no_nextpage)
    assert not click_next_page(driver)