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


def get_item_link(url, headless=False,disableimage=False):
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
    options = Options()

    options.add_argument("window-size=1920,1080")
    if headless:
        # it seems that walmart has bot detection of some sort of thing preventing the webdriver to use headless mode.
        # https://stackoverflow.com/questions/33225947/can-a-website-detect-when-you-are-using-selenium-with-chromedriver
        # https://stackoverflow.com/questions/60623059/headless-chrome-cannot-detect-elementsselenium
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    if disableimage:
        options.add_argument('--blink-settings=imagesEnabled=false')
    url_category_tuple_list = []

    driver = webdriver.Chrome(web_driver_loc, options=options)
    try:


        driver.get(url)

        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'heading-small-light'))
            WebDriverWait(driver, 5).until(element_present)
            driver.find_element_by_css_selector('.ipdetection--close.p__close').click()
        except:
            print('no pop out')
            # print(traceback.format_exc())

        category = driver.find_element_by_class_name('heading-large-thick').text
        print(category)
        page_counter = 0

        while True:
            # break the loop if it takes more than 30 seconds, return the current_url for future restart
            page_counter += 1
            loop_starting_time = int(time.time())
            time.sleep(1)
            current_url = driver.current_url
            logger.debug('current page counter: {}, url:{}'.format(page_counter,current_url))

            product_tiles = driver.find_elements_by_class_name('products-tile-list__tile')
            for tile in product_tiles:
                item_url = tile.find_element_by_css_selector('.pt--image.product-details-link').get_attribute('href')
                url_category_tuple_list.append((item_url,category))



            # go to next page
            pagination_element = driver.find_element_by_class_name('ppn--pagination')
            next_button = pagination_element.find_elements_by_tag_name('a')[1]
            if 'disabled' in next_button.get_attribute('class'):
                break
            else:
                next_button.click()
                while current_url == driver.current_url:
                    time.sleep(1)
                    #print('current:', current_url, '\nnext_url:', driver.current_url)
                    loop_lasted_time = int(time.time()) - loop_starting_time
                    if loop_lasted_time % 10 == 0: # click again in case no response
                        if current_url == next_button.get_attribute('href'):
                            logger.debug('clicked again when current url is: {}'.format(current_url))
                            next_button.click()
                    if loop_lasted_time > 60:
                        logger.error('for url:{}\ncurrent url:{}\nhas been stucked for 60 seconds, returning the current url for future restart'.format(url, current_url))
                        return current_url, url_category_tuple_list
        return True, url_category_tuple_list
    except:
        logger.error('unknow error, url:{}\n{}'.format(url, traceback.format_exc()))
        return None, url_category_tuple_list
    finally:
        driver.close()

def get_item_price(url, headless=False,disableimage=False):
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
    options = Options()

    options.add_argument("window-size=1920,1080")
    if headless:
        # it seems that walmart has bot detection of some sort of thing preventing the webdriver to use headless mode.
        # https://stackoverflow.com/questions/33225947/can-a-website-detect-when-you-are-using-selenium-with-chromedriver
        # https://stackoverflow.com/questions/60623059/headless-chrome-cannot-detect-elementsselenium
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    if disableimage:
        options.add_argument('--blink-settings=imagesEnabled=false')
    url_category_price_tuple_list = []

    driver = webdriver.Chrome(web_driver_loc, options=options)
    try:

        driver.get(url)

        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'heading-small-light'))
            WebDriverWait(driver, 5).until(element_present)
            driver.find_element_by_css_selector('.ipdetection--close.p__close').click()
        except:
            print('no pop out')
            # print(traceback.format_exc())

        category = driver.find_element_by_class_name('heading-large-thick').text
        #print(category)
        page_counter = 0

        while True:
            # break the loop if it takes more than 30 seconds, return the current_url for future restart
            page_counter += 1
            loop_starting_time = int(time.time())
            time.sleep(1)
            current_url = driver.current_url
            logger.debug('current page counter: {}, url:{}'.format(page_counter,current_url))

            product_tiles = driver.find_elements_by_class_name('products-tile-list__tile')
            for tile in product_tiles:
                item_url = tile.find_element_by_css_selector('.pt--image.product-details-link').get_attribute('href')
                prices = []
                current_price = tile.find_element_by_class_name('pi-sale-price').text
                prices.append(current_price)
                try:
                    secondary_price_element = tile.find_element_by_class_name('pi-secondary-price').find_elements_by_class_name('pi-price')
                    for price_element in secondary_price_element:
                        prices.append(price_element.text)
                except:
                    logger.debug('no secondary prices for item url:{}'.format(item_url))
                final_price = ','.join(prices)
                url_category_price_tuple_list.append((item_url,category,final_price))



            # go to next page
            pagination_element = driver.find_element_by_class_name('ppn--pagination')
            next_button = pagination_element.find_elements_by_tag_name('a')[1]
            if 'disabled' in next_button.get_attribute('class'):
                break
            else:
                next_button.click()
                while current_url == driver.current_url:
                    time.sleep(1)
                    #print('current:', current_url, '\nnext_url:', driver.current_url)
                    loop_lasted_time = int(time.time()) - loop_starting_time
                    if loop_lasted_time % 10 == 0: # click again in case no response
                        if current_url == next_button.get_attribute('href'):
                            logger.debug('clicked again when current url is: {}'.format(current_url))
                            next_button.click()
                    if loop_lasted_time > 60:
                        logger.error('for url:{}\ncurrent url:{}\nhas been stucked for 60 seconds, returning the current url for future restart'.format(url, current_url))
                        return current_url, url_category_price_tuple_list
        return True, url_category_price_tuple_list
    except:
        logger.error('unknow error, url:{}\n{}'.format(url, traceback.format_exc()))
        return None, url_category_price_tuple_list
    finally:
        driver.close()

def get_item_detail(url, headless=False,disableimage=False):
    """
    This functions create a driver based on the url string and check if there's any more subcategories under it.
    If there's any returns list of strings represents the urls,
    If not, return False
    If failed, return None
    :param url: string
    :param headless:
    :param disableimage:
    :return:
    7 element tuple list (item_url, category, name, brand, description, ingredient, img_src) item_id will then add by the caller
    None if error happened
    False if no subcategories
    """
    options = Options()

    options.add_argument("window-size=1920,1080")
    if headless:
        # it seems that walmart has bot detection of some sort of thing preventing the webdriver to use headless mode.
        # https://stackoverflow.com/questions/33225947/can-a-website-detect-when-you-are-using-selenium-with-chromedriver
        # https://stackoverflow.com/questions/60623059/headless-chrome-cannot-detect-elementsselenium
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    if disableimage:
        options.add_argument('--blink-settings=imagesEnabled=false')

    item_detail_tuple_list = []

    driver = webdriver.Chrome(web_driver_loc, options=options)
    try:

        driver.get(url)

        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'heading-small-light'))
            WebDriverWait(driver, 5).until(element_present)
            driver.find_element_by_css_selector('.ipdetection--close.p__close').click()
        except:
            print('no pop out')
            # print(traceback.format_exc())

        category = driver.find_element_by_class_name('heading-large-thick').text
        #print(category)
        page_counter = 0

        while True:
            # break the loop if it takes more than 30 seconds, return the current_url for future restart
            page_counter += 1
            loop_starting_time = int(time.time())
            time.sleep(1)
            current_url = driver.current_url
            logger.debug('current page counter: {}, url:{}'.format(page_counter,current_url))
            product_tiles = driver.find_elements_by_class_name('products-tile-list__tile')
            for tile in product_tiles:
                item_url = tile.find_element_by_css_selector('.pt--image.product-details-link').get_attribute('href')
                """prices = []
                current_price = tile.find_element_by_class_name('pi-sale-price').text
                prices.append(current_price)
                try:
                    secondary_price_element = tile.find_element_by_class_name('pi-secondary-price').find_elements_by_class_name('pi-price')
                    for price_element in secondary_price_element:
                        prices.append(price_element.text)
                except:
                    logger.debug('no secondary prices for item url:{}'.format(item_url))
                final_price = ','.join(prices)"""
                #item_detail_tuple_list.append((item_url,category,final_price))
                name = tile.find_element_by_class_name('pt-title').text

                description = tile.find_element_by_class_name('pt-weight').text
                if not description:
                    description = None
                ingredient = None
                img_element = tile.find_element_by_css_selector('.tile-product__top-section__visuals__img-product.defaultable-picture')
                img_src = img_element.find_element_by_tag_name('img').get_attribute('src')

                try:
                    brand = tile.find_element_by_class_name('pt-brand').text
                except:
                    brand = None


                item_detail_tuple_list.append((item_url, category, name, brand, description, ingredient, img_src))

            # go to next page
            pagination_element = driver.find_element_by_class_name('ppn--pagination')
            next_button = pagination_element.find_elements_by_tag_name('a')[1]
            if 'disabled' in next_button.get_attribute('class'):
                break
            else:
                next_button.click()
                while current_url == driver.current_url:
                    time.sleep(1)
                    #print('current:', current_url, '\nnext_url:', driver.current_url)
                    loop_lasted_time = int(time.time()) - loop_starting_time
                    if loop_lasted_time % 10 == 0: # click again in case no response
                        if current_url == next_button.get_attribute('href'):
                            logger.debug('clicked again when current url is: {}'.format(current_url))
                            next_button.click()
                    if loop_lasted_time > 60:
                        logger.error('for url:{}\ncurrent url:{}\nhas been stucked for 60 seconds, returning the current url for future restart'.format(url, current_url))
                        return current_url, item_detail_tuple_list
        return True, item_detail_tuple_list
    except:
        logger.error('unknow error, url:{}\n{}'.format(url, traceback.format_exc()))
        return None, item_detail_tuple_list
    finally:
        driver.close()
"""beer = 'https://www.metro.ca/en/online-grocery/aisles/beer-wine'
drink = 'https://www.metro.ca/en/online-grocery/aisles/beverages'

result = get_item_detail(beer, headless=True, disableimage=True)
for element in result:
    print(element)
print(len(result))"""