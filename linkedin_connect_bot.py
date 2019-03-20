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
    def scroll_to_button():
        SCROLL_PAUSE_TIME = 1

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    driver.get(page_url)
    random_wait()

    scroll_to_button()
    random_wait()

    html = driver.page_source
    soup = bs.BeautifulSoup(html, 'lxml')

    people_html = soup.find_all('li', 'org-people-profiles-module__profile-item')
    people_number = len(people_html)
    for i in range(1, people_number):
        try:
            connect_element = driver.find_element_by_xpath(
                '/html/body/div[5]/div[6]/div[2]/div/div[2]/div/main/div[2]/ul/li[{id}]/div/ul/li/button'.format(id=i))
            connect_element.click()

            driver.find_element_by_xpath(
                '/html/body/div[5]/div[7]/div/div[1]/div/section/div/div[2]/button[2]').click()
            print("connected")
        except:
            print("Error while connecting.")
        time.sleep(5)

    random_wait()


driver = webdriver.Firefox()
driver.maximize_window()
open_linkedin(driver)
connect_to_alumni(
    'https://www.linkedin.com/school/amirkabir-university-of-technology---tehran-polytechnic/people/?facetGeoRegion=se%3A0',
    driver)
