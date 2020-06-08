from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import logging
import traceback

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

def has_more_subcategories(url_category_tuple):
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
    driver = webdriver.Chrome(web_driver_loc)
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
        #TODO change the column in url table to unique. and test it
        pass
    else:
        logger.error('unexpected situation, num of li element is smaller than 0 for url \n{}\n the website code might have changed'.format(url))
    print(len(li_elements))
if __name__ == '__main__':
    food = 'https://www.loblaws.ca/Food/c/LSL001000000000?navid=flyout-L2-Food'
    freshfromscratch = 'https://www.loblaws.ca/Food/Meal-Kits/By-Serving-Time/Fresh-from-Scratch-(15-Min%2B)/plp/LSL001002009003?navid=CLP-L5-Fresh-from-Scratch-15-Min'
    fruit = 'https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Fruit/c/LSL001001001000?navid=CLP-L4-Fruit'
    apple = 'https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Fruit/Apples/plp/LSL001001001001?navid=CLP-L5-Apples'
    has_more_subcategories((apple,[]))