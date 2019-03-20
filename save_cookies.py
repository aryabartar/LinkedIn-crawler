import pickle

from selenium import webdriver


def open_linkedin(driver):
    def save_cookie(driver):
        pickle.dump(driver.get_cookies(), open("../cookies.pkl", "wb"))

    driver.get("https://www.linkedin.com/")
    print("Opened driver")
    input("Ready? put any button:")
    save_cookie(driver)
    driver.get("https://www.linkedin.com/")
    print("Set cookies.")


driver = webdriver.Firefox()
open_linkedin(driver)
