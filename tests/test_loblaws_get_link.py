from grocerygo_plus.grocerygo.web_crawler import has_more_subcategories, load_more, get_link, get_link_price,get_item_detail
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

import os


def test_has_more_subcategories():
    food = 'https://www.loblaws.ca/Food/c/LSL001000000000?navid=flyout-L2-Food'
    apple = 'https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Fruit/Apples/plp/LSL001001001001?navid=CLP-L5-Apples'
    assert has_more_subcategories((apple, [])) == 'Apples'
    assert has_more_subcategories((apple, []), disableimage=True) == 'Apples'
    assert has_more_subcategories((apple, []), headless=True, disableimage=True) == 'Apples'
    assert len(has_more_subcategories((food, []), headless=True, disableimage=True)) == 15


def test_load_more():
    fruit = 'https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Fruit/c/LSL001001001000?navid=CLP-L4-Fruit'
    apple = 'https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Fruit/Apples/plp/LSL001001001001?navid=CLP-L5-Apples'

    web_driver_loc = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'chromedriver.exe')

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    options.add_argument("window-size=1920,1080")
    options.add_argument('--blink-settings=imagesEnabled=false')
    driver = webdriver.Chrome(web_driver_loc, options=options)
    driver.get(fruit)
    assert load_more(driver) == 3
    driver.get(apple)
    assert load_more(driver) == 0


def test_get_link():
    fruit = 'https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Fruit/c/LSL001001001000?navid=CLP-L4-Fruit'
    apple = 'https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Fruit/Apples/plp/LSL001001001001?navid=CLP-L5-Apples'
    assert len(get_link((apple, ['test']))[0]) > 10
    assert len(get_link((fruit, ['test']), headless=True, disableimage=True)[0]) > 100
    assert get_link((apple, ['test']), headless=True, disableimage=True)[1][0] == 'test'


def test_get_link_price():
    fruit = 'https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Fruit/c/LSL001001001000?navid=CLP-L4-Fruit'
    apple = 'https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Fruit/Apples/plp/LSL001001001001?navid=CLP-L5-Apples'
    assert len(get_link_price((apple, ['test']))) > 10
    fruit_result = get_link_price((fruit, ['test']), headless=True, disableimage=True)
    assert len(fruit_result) > 100
    for result in fruit_result:
        assert '$' in result[2]
    assert get_link_price((apple, ['test']), headless=True, disableimage=True)[0][1][0] == 'test'


def test_get_item_detail():
    unavailable = 'https://www.loblaws.ca/Food/Ready-Made-Meals/Ready-Meals-%26-Sides/Sushi-%26-Bento/Spicy-Salmon-Roll/p/20072659_EA'
    has_all = 'https://www.loblaws.ca/Food/Frozen/Ice-Cream-%26-Treats/Ice-Cream-Tubs-%26-Treats/Strawberry-Ice-Cream/p/20322906_EA'
    no_des = "https://www.loblaws.ca/Food/Frozen/Vegetables/Vegetable-Bags/President's-Choice-Sliced-Red-Beets/p/21106753_EA"
    no_b_no_ing = 'https://www.loblaws.ca/Food/Ready-Made-Meals/Ready-Meals-%26-Sides/Chicken-%26-Turkey-Meals-(hot-foods-for-pickup-after-12PM)/1-Original-Chicken-Tender/p/20077463_EA'
    assert get_item_detail((1, unavailable), headless=True, disableimage=True) == 'unavailable'
    assert not all(get_item_detail((1, has_all), headless=True, disableimage=True))
    assert get_item_detail((1, no_des), headless=True, disableimage=True)[3] is None
    result = get_item_detail((1, no_b_no_ing), headless=True, disableimage=True)
    assert result[2] is None
    assert result[4] is None
