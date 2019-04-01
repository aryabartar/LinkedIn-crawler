import pickle
import time
import os
from random import randint

from selenium import webdriver


def append_to_file(path, text):
    f = open(path, "a")
    f.write(text)
    f.close()


def read_file(path):
    try:
        f = open(path, "r", encoding="utf-8")
        text = f.read()
        f.close()
        return text

    except Exception as e:
        print(e)


def write_to_file(path, text, is_binary=False):
    if is_binary:
        f = open(path, "wb")
        f.write(text)
        f.close()

    else:
        f = open(path, "w+")
        f.write(text)
        f.close()


def open_linkedin():
    def restore_cookie(driver):
        cookies = pickle.load(open("../cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)

    driver = webdriver.Firefox()
    driver.maximize_window()

    driver.get("https://www.linkedin.com/")
    print("Opened driver")

    restore_cookie(driver)

    driver.get("https://www.linkedin.com/")
    print("Set cookies.")

    return driver


def scroll_to_button(driver, number_of_scrolls, slow_scroll=False):
    number_of_scrolls = int(number_of_scrolls)
    counter = 0

    while True:
        if slow_scroll:
            time.sleep(randint(10, 28))
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


def make_dir(path):
    try:
        os.mkdir(path)
    except:
        pass

    return path
