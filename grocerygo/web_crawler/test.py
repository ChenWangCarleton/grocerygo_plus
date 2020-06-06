from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os

web_driver_loc = os.path.join(os.path.abspath(os.path.dirname(__file__)),'chromedriver.exe')
print(web_driver_loc)
driver = webdriver.Chrome(web_driver_loc)
driver.get("https://www.python.org")
print(driver.title)