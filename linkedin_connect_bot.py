import time
import pickle
import bs4 as bs
import csv
import glob

from random import randint
from selenium import webdriver


def append_to_file(path, text):
    f = open(path, "a")
    f.write(text)
    f.close()


def open_linkedin(driver):
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
    random = randint(5, 10)
    time.sleep(random)


def connect_to_alumni(page_url, driver):
    def scroll_to_button(number_of_scrolls):
        number_of_scrolls = int(number_of_scrolls)
        counter = 0

        while True:
            time.sleep(1)

            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            if counter == number_of_scrolls:
                break

            counter += 1

    def remove_first_and_last_spaces(text):
        # removes name spaces and \n
        text = text.replace("\n", " ")
        for i in range(0, len(text)):
            if text[i] != " ":
                break
        text = text[i:]

        for i in range(len(text) - 1, 0, -1):
            if text[i] != " ":
                break
        text = text[:i + 1]
        return text

    driver.get(page_url)
    random_wait()

    html = driver.page_source
    soup = bs.BeautifulSoup(html, 'lxml')

    alumni_number = soup.find('span', {"class": "t-20"}).text
    alumni_number = remove_first_and_last_spaces(alumni_number)
    scroll_number = int(int(alumni_number.split(' ')[0]) / 12)
    print("Scroll Number: ", scroll_number, " |Alumni number: ", alumni_number)

    # scroll_to_button(scroll_number)
    random_wait()

    html = driver.page_source
    soup = bs.BeautifulSoup(html, 'lxml')

    people_html = soup.find_all('div', {"class": "org-people-profile-card__profile-title"})
    people_number = len(people_html)

    for i in range(0, people_number - 1):
        # try:
        try:
            # Notification when connecting much.
            driver.find_element_by_class_name('ip-fuse-limit-alert__primary-action').click()
            print("Clicked on notification button. ")
        except:
            pass

        profile_name = people_html[i]
        print(profile_name)

        connect_element = driver.find_element_by_xpath(
            '/html/body/div[5]/div[6]/div[2]/div/div[2]/div/main/div[2]/ul/li[{id}]/div/ul/li/button'.format(
                id=i + 1))

        connect_element.click()

        driver.find_element_by_xpath(
            '/html/body/div[5]/div[7]/div/div[1]/div/section/div/div[2]/button[2]').click()

        print("connected")
        # except:
        #     print("Error while connecting.")
        time.sleep(2)

        random_wait()


driver = webdriver.Firefox()
driver.maximize_window()
open_linkedin(driver)
connect_to_alumni(
    'https://www.linkedin.com/school/amirkabir-university-of-technology---tehran-polytechnic/people/?facetGeoRegion=se%3A0',
    driver)
