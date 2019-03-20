import time
import pickle
import bs4 as bs
import csv
import glob

from random import randint
from selenium import webdriver


def open_linkedin(driver):
    def save_cookie(driver):
        pickle.dump(driver.get_cookies(), open("../cookies.pkl", "wb"))

    def restore_cookie(driver):
        cookies = pickle.load(open("../cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)

    driver.get("https://www.linkedin.com/")
    print("Opened driver")

    restore_cookie(driver)

    driver.get("https://www.linkedin.com/")
    print("Set cookies.")


def random_wait():
    random = randint(3, 6)
    time.sleep(random)


def connect_to_alumni(page_url, driver):
    driver.get(page_url)
    element = driver.find_element_by_xpath(
        '/html/body/div[5]/div[6]/div[2]/div/div[2]/div/main/div[2]/ul/li[1]/div/ul/li/button')
        '/html/body/div[5]/div[6]/div[2]/div/div[2]/div/main/div[2]/ul/li[8]/div/ul/li/button')

    element.click()
    random_wait()


driver = webdriver.Firefox()
driver.maximize_window()
open_linkedin(driver)
connect_to_alumni(
    'https://www.linkedin.com/school/amirkabir-university-of-technology---tehran-polytechnic/people/?facetGeoRegion=se%3A0',
    driver)
