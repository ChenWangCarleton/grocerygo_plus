from grocerygo_plus.grocerygo.web_crawler.utils_walmart import has_subcategory, click_next_page, get_item_link, \
    get_item_link_price, get_item_detail, get_all_category_link, get_all_category_price
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


def test_get_item_link():
    url_42items = 'https://www.walmart.ca/en/grocery/frozen-food/ice-cream-treats/ice-cream-tubs/N-9394'
    web_driver_loc = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'chromedriver.exe')

    options = Options()
    options.add_argument('--blink-settings=imagesEnabled=false')
    driver = webdriver.Chrome(web_driver_loc, options=options)
    driver.get(url_42items)
    assert len(get_item_link(driver)) == 42


def test_get_item_link_price():
    url_42items = 'https://www.walmart.ca/en/grocery/frozen-food/ice-cream-treats/ice-cream-tubs/N-9394'
    web_driver_loc = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'chromedriver.exe')

    options = Options()
    options.add_argument('--blink-settings=imagesEnabled=false')
    driver = webdriver.Chrome(web_driver_loc, options=options)
    driver.get(url_42items)
    result = get_item_link_price(driver)
    assert len(result) == 42
    for one in result:
        assert one[2]


def test_get_item_detail():
    item_d_all = 'https://www.walmart.ca/en/ip/great-value-honey-greek-yogurt-smoothie-bars/6000200313230'
    item_d_nod_nob_noI = 'https://www.walmart.ca/en/ip/pears-bartlett/6000187833002'
    result = get_item_detail((1, item_d_all), disableimage=True)
    for attr in result:
        assert attr
    result = get_item_detail((1, item_d_nod_nob_noI), disableimage=True)
    assert result[2] is None
    assert result[3] is None
    assert result[4] is None


def test_get_all_category_link():
    more_than_60 = 'https://www.walmart.ca/en/grocery/frozen-food/frozen-pizza/N-3832'
    result = get_all_category_link(more_than_60, disableimage=True)
    assert len(result) > 60

def test_get_all_category_price():
    more_than_60 = 'https://www.walmart.ca/en/grocery/frozen-food/frozen-pizza/N-3832'
    result = get_all_category_price(more_than_60, disableimage=True)
    assert len(result) > 60
    for one in result:
        assert one[2]
