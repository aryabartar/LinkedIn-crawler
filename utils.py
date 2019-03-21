import pickle

from selenium import webdriver


def append_to_file(path, text):
    f = open(path, "a")
    f.write(text)
    f.close()


def read_file(path):
    try:
        f = open(path, "r")
        text = f.read()
        f.close()
        return text

    except Exception as e:
        f = open(path, "w+")
        f.close()
        return ""


def write_to_file(path, text):
    f = open(path, "w")
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
