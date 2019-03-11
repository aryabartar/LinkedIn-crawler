import pickle
from selenium import webdriver

import time


def open_linkedin():
    def save_cookie(driver):
        pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

    def restore_cookie(driver):
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)

    driver = webdriver.Firefox()
    driver.get("https://www.linkedin.com/")
    restore_cookie(driver)
    driver.get("https://www.linkedin.com/")

open_linkedin()