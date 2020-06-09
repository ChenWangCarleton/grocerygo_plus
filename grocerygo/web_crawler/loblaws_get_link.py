from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import logging
import traceback
import time

import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


web_driver_loc = os.path.join(os.path.abspath(os.path.dirname(__file__)),'chromedriver.exe')
max_running_thread = 10
waiting_list = [] # a list contains thread to be executed to get item links of each leaf categories

def load_more(driver):
    """
    This function loads all the "load xxx more results" on the page untill all the items are loaded
    Then it returns the total times of load button clicked successfully if there was any
    Otherwise it returns 0

    The function is implemented by checking if backslash exists in pagination,
    no backslash example(1-166 Results) with backslash example (1-48 / 156 Results)
    if there is backslash in pagination, then it means load more button should be clickable,
    click and repeat untill no more backslash in pagination or time limit reached
    :param driver: the driver instance that should be the leaf category webpage
    :return:
        int
            number of times the load more button been pressed
    """
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'pagination'))
        WebDriverWait(driver, 10).until(element_present)
    except:
        logger.error('time limit exceeds when waiting for loading total number of items\n{}\n{}'.driver.getCurrentUrl(), traceback.format_exc())
    current_pagination = driver.find_element_by_class_name('pagination').text
    click_counter = 0

    while '/' in current_pagination:
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'load-more-button'))
            WebDriverWait(driver, 10).until(element_present)
        except:
            logger.error('time limit exceeds when waiting for load more buttion to appear on page\n{}\n{}'.format(driver.getCurrentUrl(), traceback.format_exc()))
            return False
        load_more_button = driver.find_element_by_class_name('load-more-button')
        load_more_button.click()
        time.sleep(1)
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'pagination'))
            WebDriverWait(driver, 10).until(element_present)
        except:
            logger.error('time limit exceeds when waiting for loading pagination after clicking load more button. button click counter {}\n{}\n{}'.format(click_counter,driver.getCurrentUrl(),
                traceback.format_exc()))
        current_pagination = driver.find_element_by_class_name('pagination').text
        click_counter = click_counter + 1
    return click_counter
def has_more_subcategories(url_category_tuple,headless=False,disableimage=False): #
    """
    This function checks if there are more subcategories in the url.
    If there is any, it returns the list of 2 element tuple. The first element in the tuple is the url,
    the second element in the tuple is a list of all category
    If not, it returns string which is the current category
    :param url: the url of the webpage, it should be one of the webpage under food category from loblaws
    :return:
        list
            a list of 2-element-tuple of url as first value , list of categories as second value, the current category is appended to the end of the list of categories
        string
            string of the current category if there is no more subcategories
    """
    url = url_category_tuple[0]
    options = Options()
    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')  # Last I checked this was necessary.
        options.add_argument("window-size=1920,1080")
    if disableimage:
        options.add_argument('--blink-settings=imagesEnabled=false')

    driver = webdriver.Chrome(web_driver_loc, options=options)
    driver.get(url)
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'category-filter__subcategories'))
        WebDriverWait(driver, 10).until(element_present)
    except:
        logger.error('error when waiting for element on url:\n{}\n{}'.format(url, traceback.format_exc()))
    subcategories_class = driver.find_element_by_class_name('category-filter__subcategories')
    li_elements = subcategories_class.find_elements_by_tag_name('li')
    current_category = li_elements[0].text
    print(current_category)
    if len(li_elements) == 1:
        logger.info('No more subcategory under category: {} with url:\n{}'.format(url, current_category))
        return current_category
    elif len(li_elements) > 1:
        result_list = []
        for i in range(1, len(li_elements)):

            sub_category_url = li_elements[i].find_element_by_tag_name('a').get_attribute('href')
            logger.debug(sub_category_url)
            temp_category_list = url_category_tuple[1].copy()
            temp_category_list.append(current_category)
            result_list.append((sub_category_url, temp_category_list))
        return result_list
    else:
        logger.error('unexpected situation, num of li element is smaller than 0 for url \n{}\n the website code might have changed'.format(url))
    print(len(li_elements))
if __name__ == '__main__':
    food = 'https://www.loblaws.ca/Food/c/LSL001000000000?navid=flyout-L2-Food'
    freshfromscratch = 'https://www.loblaws.ca/Food/Meal-Kits/By-Serving-Time/Fresh-from-Scratch-(15-Min%2B)/plp/LSL001002009003?navid=CLP-L5-Fresh-from-Scratch-15-Min'
    fruit = 'https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Fruit/c/LSL001001001000?navid=CLP-L4-Fruit'
    apple = 'https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Fruit/Apples/plp/LSL001001001001?navid=CLP-L5-Apples'
    #print(has_more_subcategories((apple,[])))

    options = Options()
    options.add_argument('--blink-settings=imagesEnabled=false')
    driver = webdriver.Chrome(web_driver_loc, options=options)
    driver.get(fruit)
    print(load_more(driver))
    driver.get(apple)
    print(load_more(driver))
