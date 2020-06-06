from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By
import os

web_driver_loc = os.path.join(os.path.abspath(os.path.dirname(__file__)),'chromedriver.exe')
print(web_driver_loc)
driver = webdriver.Chrome(web_driver_loc)
driver.get("https://www.loblaws.ca/Food/Deli/Deli-Meats/Beef/Ziggy's-Smoked-Beef-Pastrami/p/21020569_KG")
print(driver.title)
cookies_list = driver.get_cookies()
cookies_dict = {}
for cookie in cookies_list:
    cookies_dict[cookie['name']] = cookie['value']

print(cookies_dict)
element_present = EC.presence_of_element_located((By.LINK_TEXT, 'choose the location'))
WebDriverWait(driver, 10).until(element_present)
link = driver.find_element_by_link_text('choose the location')
link.click()
element_present = EC.presence_of_element_located((By.CLASS_NAME, 'location-list-item__actions'))
WebDriverWait(driver, 10).until(element_present)
a = driver.find_elements_by_class_name("location-list-item__actions")
a[3].click()
element_present = EC.presence_of_element_located((By.LINK_TEXT, 'Continue'))
WebDriverWait(driver, 10).until(element_present)
link = driver.find_element_by_link_text('Continue')
link.click()

print(driver.title)
cookies_list = driver.get_cookies()
isabella_dict = {}
for cookie in cookies_list:
    isabella_dict[cookie['name']] = cookie['value']

print(isabella_dict)
#driver.get("https://www.loblaws.ca/Food/Bakery/Desserts-%26-Pastries/Pastries-%26-Danishes/Sikorski-Sausages-Double-Smoked-Bacon/p/20996153_KG")


driver_2 = webdriver.Chrome(web_driver_loc)
driver_2.get("https://www.loblaws.ca/Food/Deli/Deli-Meats/Beef/Ziggy's-Smoked-Beef-Pastrami/p/21020569_KG")
print(driver_2.title)
cookies_list = driver_2.get_cookies()
cookies_dict = {}
for cookie in cookies_list:
    cookies_dict[cookie['name']] = cookie['value']

print(cookies_dict)
element_present = EC.presence_of_element_located((By.LINK_TEXT, 'choose the location'))
WebDriverWait(driver_2, 10).until(element_present)
link = driver_2.find_element_by_link_text('choose the location')
link.click()
element_present = EC.presence_of_element_located((By.CLASS_NAME, 'location-list-item__actions'))
WebDriverWait(driver_2, 10).until(element_present)
a = driver_2.find_elements_by_class_name("location-list-item__actions")
a[0].click()
element_present = EC.presence_of_element_located((By.LINK_TEXT, 'Continue'))
WebDriverWait(driver_2, 10).until(element_present)
link = driver_2.find_element_by_link_text('Continue')
link.click()

print(driver_2.title)
cookies_list = driver_2.get_cookies()
bank_dict = {}
for cookie in cookies_list:
    bank_dict[cookie['name']] = cookie['value']

print(bank_dict)

set1 = set(bank_dict.items())
set2 = set(isabella_dict.items())
print(set1 ^ set2)
driver.get("https://www.loblaws.ca/Food/Deli/Deli-Meats/Beef/Ziggy's-Smoked-Beef-Pastrami/p/21020569_KG")
