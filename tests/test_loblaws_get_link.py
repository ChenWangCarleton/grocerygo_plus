from grocerygo_plus.grocerygo.web_crawler import has_more_subcategories, load_more, get_link
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
    assert len(get_link((apple,['test']))[0]) > 10
    assert len(get_link((fruit,['test']),headless=True,disableimage=True)[0]) > 100
    assert get_link((apple,['test']),headless=True,disableimage=True)[1][0] =='test'
