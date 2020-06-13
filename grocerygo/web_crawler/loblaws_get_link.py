import logging
import traceback
import time
import os

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

def get_item_detail(id_url_tuple, headless=False, disableimage=False):
    """
    This function gets the item detail from giving id_url_tuple which is a 2-element tuple that
    the first element is the item_id, the second element is the url of the item page.
    The function first check if the url is redirected to loblaws homepage which means the item is not available at the moment,
    if so return string unavailable
    If not, collect the item name, brand if exist, description if exist, ingrident list if exist
    then return a 6-element tuple (item_id, name, brand, description, ingrident, imgsrc)
    Return False when unexpected error happens
    :param id_url_tuple: a 2-element tuple that
    the first element is the item_id, the second element is the url of the item page.
    :param headless: boolen for representing whether it runs in headless mode
    :param disableimage: boolen for representing whether it runs in image-less mode
    :return:
    String unavailable when page not available
    False when error happens
    Tuple a 6-element tuple (item_id, name, brand, description, ingrident, imgsrc)
    """
    item_id = id_url_tuple[0]
    url = id_url_tuple[1]
    options = Options()
    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')  # Last I checked this was necessary.
        options.add_argument("window-size=1920,1080")
    if disableimage:
        options.add_argument('--blink-settings=imagesEnabled=false')

    driver = webdriver.Chrome(web_driver_loc, options=options)
    try:
        driver.get(url)
        driver.implicitly_wait(1)
        home_page = 'https://www.loblaws.ca/'
        unavailable_msg = 'unavailable'
        if home_page == driver.current_url:
            logger.debug('Item page unavailable for id: {} url: \n{}'.format(item_id, url))
            return unavailable_msg

        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'product-details-page-details__content__name'))
        WebDriverWait(driver, 10).until(element_present)

        current_item_element = driver.find_element_by_class_name('product-details-page-details__content__name')
        name = current_item_element.find_element_by_css_selector('.product-name__item.product-name__item--name').text
        brand = None
        try:
            selenium_input = '.product-name__item.product-name__item--brand'
            element_present = EC.presence_of_element_located(
                (By.CSS_SELECTOR, selenium_input))
            WebDriverWait(driver, 2).until(element_present)
            brand = current_item_element.find_element_by_css_selector(selenium_input).text
        except (NoSuchElementException, TimeoutException) as e:
            logger.debug('no brand info for id: {} url: \n{}'.format(item_id, url))
        description = None
        try:
            selenium_input = 'product-description-text__text'
            element_present = EC.presence_of_element_located(
                (By.CLASS_NAME, selenium_input))
            WebDriverWait(driver, 2).until(element_present)

            description = driver.find_element_by_class_name(selenium_input).text
        except (NoSuchElementException, TimeoutException) as e:
            logger.debug('no description for id: {} url: \n{}'.format(item_id, url))
        ingredients = None
        try:
            """class_name = "product-details-page-info-layout-content product-details-page-info-layout-content--i product-details-page-info-layout-content--n product-details-page-info-layout-content--g product-details-page-info-layout-content--r product-details-page-info-layout-content--e product-details-page-info-layout-content--d product-details-page-info-layout-content--i product-details-page-info-layout-content--e product-details-page-info-layout-content--n product-details-page-info-layout-content--t product-details-page-info-layout-content--s product-details-page-info-layout-content--active"
            class_name = '.'+'.'.join(class_name.split(' '))
            print(class_name)
            selenium_input = class_name"""
            selenium_input = '.product-details-page-info-layout.product-details-page-info-layout--ingredients'
            element_present = EC.presence_of_element_located(
                (By.CSS_SELECTOR, selenium_input))
            WebDriverWait(driver, 2).until(element_present)
            ingredients = driver.find_element_by_css_selector(selenium_input).find_element_by_tag_name('div').get_attribute('innerHTML')
            # here it seems only works with innerHTML istead of text
            #print('ingredi:',ingredients.get_attribute('innerHTML'))
            #ingredients = driver.find_element_by_css_selector('.product-details-page-info-layout.product-details-page-info-layout--ingredients').text
        except (NoSuchElementException, TimeoutException) as e:
            logger.debug('no ingredients for id: {} url: \n{}'.format(item_id, url))
        imgsrc = None
        try:
            selenium_input = '.product-image-list__item.product-image-list__item--product-details-page.product-image-list__item--0'
            element_present = EC.presence_of_element_located(
                (By.CSS_SELECTOR, selenium_input))
            WebDriverWait(driver, 2).until(element_present)
            image_element = driver.find_elements_by_css_selector(selenium_input)[0]
            imgsrc = image_element.find_element_by_tag_name('img').get_attribute('src')
            print(imgsrc)
        except (NoSuchElementException, TimeoutException) as e:
            logger.debug('no image src found for id: {} url: \n{}'.format(item_id, url))
        result_tuple = (item_id,name,brand,description,ingredients, imgsrc)
        logger.debug('item detail got for id: {} url: \n{}\nvalue:{}'.format(item_id, url,result_tuple))
        #input('hrere')
        return result_tuple

    except:
        logger.error('error when getting item detail for id:{}  url:\n{}\n{}'.format(item_id, url,traceback.format_exc()))
        return False




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


def get_link_price(url_category_tuple,headless=False,disableimage=False):
    """
    This function creates a driver using the url from the first element in the parameter url_category_tuple and
    gets all the listed items' item-page-url, category list and prices

    :param url_category_tuple: a 2-element-tuple that
        the first element is the url of the webpage,
        it should be one of the webpage under food category from loblaws.
        the second element is the category list, which is a list of strings

    :param headless: boolen for representing whether it runs in headless mode
    :param disableimage: boolen for representing whether it runs in image-less mode
    :return: a 3-element tuple list which the first element is the item page url,
        the second element is the category list from the second element in the parameter url_category_tuple,
        the third element is the current presented price & other formats of the presented price if any separated by comma
        boolean False when error happened
    """
    url = url_category_tuple[0]
    category_list = url_category_tuple[1]
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
        item_elements = driver.find_elements_by_class_name('product-tile__details')

        if len(item_elements) != total_item_listed:
            # do it again if it does not match :)
            time.sleep(1)
            item_elements = driver.find_elements_by_class_name('product-tile__details')
            if len(item_elements) != total_item_listed:
                logger.error('total number of item showing in pagination does not match with items found in page'
                             ' when getting itempage urls for url:\n{}\n{}'.format(url, traceback.format_exc()))
                return False

        result_list = []
        print(len(item_elements))
        for element in item_elements:

            itempage_url = element.find_element_by_class_name('product-tile__details__info__name__link').get_attribute('href')
            current_price = element.find_element_by_css_selector('.price.selling-price-list__item__price.selling-price-list__item__price--now-price').text
            comparison_price = element.find_element_by_css_selector('.comparison-price-list.comparison-price-list--product-tile.comparison-price-list--product-tile').text
            cp_list = comparison_price.split('$')
            return_price = current_price
            if len(cp_list) > 1:
                for i in range(1, len(cp_list)):
                    return_price = return_price + ',$' + cp_list[i]
            """print('current price:{}:'.format(current_price))
            print('comparison_price:',comparison_price)
            print(return_price)"""
            result_list.append((itempage_url,category_list,return_price))
        logger.info("all itempages' link collected in url\n{}".format(url))
        return result_list

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
#get_link_price(('https://www.loblaws.ca/Food/Deli/Deli-Meats/Beef/plp/LSL001002001002?navid=CLP-L5-Beef',[]))

#print(get_link_price(('https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Organic-Vegetables/plp/LSL001001006000',['test'])))