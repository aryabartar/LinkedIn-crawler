import time
import pickle

from random import randint
from selenium import webdriver


def random_wait():
    random = randint(1, 5)
    time.sleep(random)


def open_linkedin(driver):
    def save_cookie(driver):
        pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

    def restore_cookie(driver):
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)

    driver.get("https://www.linkedin.com/")
    restore_cookie(driver)
    driver.get("https://www.linkedin.com/")


def open_amirkabir_alumni(driver):
    pass

driver = webdriver.Firefox()
open_linkedin(driver)
random_wait()
open_amirkabir_alumni(driver)
