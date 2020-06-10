import logging
import traceback
import time
import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options



logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


web_driver_loc = os.path.join(os.path.abspath(os.path.dirname(__file__)),'chromedriver.exe')


def get_link(url_category_tuple,headless=False,disableimage=False):
    """
    This function creates a driver using the url from the first element in the parameter url_category_tuple and
    gets all the listed items' item-page-url

    :param url_category_tuple: a 2-element-tuple that
        the first element is the url of the webpage,
        it should be one of the webpage under food category from loblaws.
        the second element is the category list, which is a list of strings

    :param headless: boolen for representing whether it runs in headless mode
    :param disableimage: boolen for representing whether it runs in image-less mode
    :return: a 2-element tuple which the first element is a list of urls,
        the second element is the category list from the second element in the parameter url_category_tuple
        boolean False when error happened
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

    result = load_more(driver)

    logger.debug('load more button clicked total {} times for url:\n{}'.format(result,url))

    try:
        current_pagination = driver.find_element_by_class_name('pagination').text
        total_item_listed = int(current_pagination[2:].split(' ')[0])
        item_elements = driver.find_elements_by_class_name('product-tile__details__info__name__link')

        if len(item_elements) != total_item_listed:
            # do it again if it does not match :)
            time.sleep(1)
            item_elements = driver.find_elements_by_class_name('product-tile__details__info__name__link')
            if len(item_elements) != total_item_listed:
                logger.error('total number of item showing in pagination does not match with items found in page'
                             ' when getting itempage urls for url:\n{}\n{}'.format(url, traceback.format_exc()))
                return False

        url_list = []
        for element in item_elements:
            itempage_url = element.get_attribute('href')
            url_list.append(itempage_url)
        logger.info("all itempages' link collected in url\n{}".format(url))
        return (url_list,url_category_tuple[1])

    except:
        logger.error('error when getting itempage urls for url:\n{}\n{}'.format(url,traceback.format_exc()))
        return False



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


def has_more_subcategories(url_category_tuple,headless=False,disableimage=False):
    """
    This function checks if there are more subcategories in the url.

    If there is any, it returns the list of 2 element tuple. The first element in the tuple is the url,
    the second element in the tuple is a list of all category

    If not, it returns string which is the current category, the function caller should
    then add the current category to category list

    :param url_category_tuple: a 2-element-tuple that
        the first element is the url of the webpage,
        it should be one of the webpage under food category from loblaws.
        the second element is the category list, which is a list of strings

    :param headless: boolen for representing whether it runs in headless mode
    :param disableimage: boolen for representing whether it runs in image-less mode
    :return:
        list
            a list of 2-element-tuple of url as first value , list of categories as second value, the current category is appended to the end of the list of categories
        string
            string of the current category if there is no more subcategories
        boolean False when error happened
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
        return False
