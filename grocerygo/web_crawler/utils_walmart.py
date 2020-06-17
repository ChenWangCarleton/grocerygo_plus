import logging
import traceback
import time
import os
import re

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


web_driver_loc = os.path.join(os.path.abspath(os.path.dirname(__file__)),'chromedriver.exe')

walmart_root_categories = ['https://www.walmart.ca/en/grocery/fruits-vegetables/N-3799',
                           'https://www.walmart.ca/en/grocery/dairy-eggs/N-3798',
                           'https://www.walmart.ca/en/grocery/meat-seafood/N-3793',
                           'https://www.walmart.ca/en/grocery/natural-organic-food/N-3992',
                           'https://www.walmart.ca/en/grocery/pantry-food/N-3794',
                           'https://www.walmart.ca/en/grocery/international-foods/N-4356',
                           'https://www.walmart.ca/en/grocery/frozen-food/N-3795',
                           'https://www.walmart.ca/en/grocery/frozen-food/ice-cream-treats/N-3828',
                           'https://www.walmart.ca/en/grocery/pantry-food/chips-snacks/N-3842',
                           'https://www.walmart.ca/en/grocery/pantry-food/cereal-breakfast/N-3830',
                           'https://www.walmart.ca/en/grocery/deli-ready-made-meals/N-3792',
                           'https://www.walmart.ca/en/grocery/bakery/N-3796',
                           'https://www.walmart.ca/en/grocery/drinks/N-3791']

def has_subcategory(url, headless=False,disableimage=False):
    """
    This functions create a driver based on the url string and check if there's any more subcategories under it.
    If there's any returns list of strings represents the urls,
    If not, return False
    If failed, return None
    :param url: string
    :param headless:
    :param disableimage:
    :return:
    A list of strings(urls) if it has subcategories,
    None if error happened
    False if no subcategories
    """
    magic_index = 1
    options = Options()
    if headless:
        # it seems that walmart has bot detection of some sort of thing preventing the webdriver to use headless mode.
        # https://stackoverflow.com/questions/33225947/can-a-website-detect-when-you-are-using-selenium-with-chromedriver
        # https://stackoverflow.com/questions/60623059/headless-chrome-cannot-detect-elementsselenium
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')  # Last I checked this was necessary.
        options.add_argument("window-size=1920,1080")
        magic_index = 0
    if disableimage:
        options.add_argument('--blink-settings=imagesEnabled=false')

    driver = webdriver.Chrome(web_driver_loc, options=options)
    try:
        driver.get(url)
        level_css_selecter_template = '.category-list.l-{}.collapsed'
        #driver.save_screenshot("screenshot_{}.png".format(headless))
        base_element = driver.find_elements_by_class_name('selected')[magic_index]
        #print(driver.find_element_by_css_selector('.category-list.l-3.collapsed').get_attribute('class'))
        #print(base_elements[1].text)
        parent = base_element.find_element_by_xpath('..').find_element_by_xpath('..')
        selected_level = re.search(r'category-list l-(.*?) collapsed', parent.get_attribute('class')).group(1)
        try:
            sub_root = driver.find_element_by_css_selector(level_css_selecter_template.format(int(selected_level)+1))

            result_list = []
            sub_elements = sub_root.find_elements_by_class_name('link')
            for element in sub_elements:
                result_list.append(element.get_attribute('href'))
            logger.debug('has {} more subcategory for url: {}\n{}'.format(len(result_list), url,result_list))
            #print(result_list)
            return result_list
        except NoSuchElementException:
            logger.debug('no more subcategory for url: {}'.format(url))
            return False
        #print(parent.get_attribute('class'))
        #print(re.search(r'category-list l-(.*?) collapsed', parent.get_attribute('class')).group(1))
        """for base in base_elements:
            print(base.text)
            parent = base.find_element_by_xpath('..').find_element_by_xpath('..')
            print(parent.get_attribute('class'))"""

    except:
        logger.error('unexpected error in has_more_subcategories with url\n{}\n{}'.format(url,traceback.format_exc()))
        return None
    finally:
        driver.close()


def click_next_page(driver):
    """
    This function checks if there is next page in the current page opened in driver.
    If there is, click next page and return True
    If not, return False,
    If unexpected error happens, return None
    :param driver:
    :return:
    Boolean True if there is next page and clicked
    Boolean False if there is no more next page
    None if unexpected error happens
    """
    try:
        element_present = EC.presence_of_element_located((By.ID, 'shelf-sort-count'))
        WebDriverWait(driver, 10).until(element_present)
        pagination = driver.find_element_by_id('shelf-sort-count')
        last_page_number = pagination.find_element_by_class_name('last-rec-num').text
        total_page_number = pagination.find_element_by_class_name('total-num-recs').text
        if last_page_number == total_page_number:
            logger.debug('no next page for url: {}'.format(driver.current_url))
            return False
        else:
            # driver.find_element_by_class_name('page-select-list-btn').click()
            # clicking the webelement didn't work due to error
            """
            selenium.common.exceptions.ElementClickInterceptedException: Message: element click intercepted: Element <a href="/en/grocery/pantry-food/chips-snacks/fruit-snacks/N-3782/page-2" id="loadmore" class="page-select-list-btn" attr-page-id="1" aria-label="Next 60 items" analytics-trigger="search" analytics-data="next results page">...</a> is not clickable at point (543, 906). Other element would receive the click: <div class="privacy-copy">...</div>
            (Session info: chrome=83.0.4103.97)
            """
            # thus, getting the next page's url and load the page with driver
            next_page_url = driver.find_element_by_class_name('page-select-list-btn').get_attribute('href')
            driver.get(next_page_url)

            # wait till the page fully loaded before returning
            element_present = EC.presence_of_element_located((By.ID, 'shelf-sort-count'))
            WebDriverWait(driver, 10).until(element_present)

            logger.debug('next page clicked for url: {}'.format(driver.current_url))
            return True
    except:
        logger.error('unexpected error in click_next_page with url\n{}\n{}'.format(driver.current_url, traceback.format_exc()))
        return None
