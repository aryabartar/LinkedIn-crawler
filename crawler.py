import time
import pickle

from random import randint
from selenium import webdriver


def random_wait():
    random = randint(1, 3)
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


def get_amirkabir_alumni_html(driver):
    aut_usa_url = "https://www.linkedin.com/school/amirkabir-university-of-technology---tehran-polytechnic/people/?facetGeoRegion=us%3A0"
    driver.get(aut_usa_url)
    return driver.page_source


def find_names_from_main_page(html):
    names_list = []

    html = html.replace("\n", " ").split(" ")
    while "lt-line-clamp--single-line" in html:
        index = html.index(
            'lt-line-clamp--single-line')
        name = "{firstname} {lastname}".format(firstname=html[index + 3], lastname=html[index + 4])
        del html[index]
        names_list.append(name)

    return names_list


driver = webdriver.Firefox()
open_linkedin(driver)
random_wait()
amirkabir_alumni_html = get_amirkabir_alumni_html(driver)
print(find_names_from_main_page(amirkabir_alumni_html))
