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

def has_more_subcategories(url):
    """
    This function checks if there are more subcategories in the url. If there is any, it returns the list of urls of the them.
    If not, it returns False
    :param url: the url of the webpage, it should be one of the webpage under food category from loblaws
    :return:
        list
            a list of urls if there are subcategories
        false
            False if there is no more subcategories
    """
    driver = webdriver.Chrome(web_driver_loc)
    driver.get(url)
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'category-filter__subcategories'))
        WebDriverWait(driver, 10).until(element_present)
    except:
        logger.error('error when waiting for element on url:\n{}\n{}'.format(url, traceback.format_exc()))
if __name__ == '__main__':
    food = 'https://www.loblaws.ca/Food/c/LSL001000000000?navid=flyout-L2-Food'
    freshfromscratch = 'https://www.loblaws.ca/Food/Meal-Kits/By-Serving-Time/Fresh-from-Scratch-(15-Min%2B)/plp/LSL001002009003?navid=CLP-L5-Fresh-from-Scratch-15-Min'
    fruit = 'https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Fruit/c/LSL001001001000?navid=CLP-L4-Fruit'
    apple = 'https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Fruit/Apples/plp/LSL001001001001?navid=CLP-L5-Apples'
    has_more_subcategories(food)