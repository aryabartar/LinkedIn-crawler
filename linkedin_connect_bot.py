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

def connect_to_alumni():
    pass

driver = webdriver.Firefox()
open_linkedin(driver)
connect_to_alumni ()