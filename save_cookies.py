import pickle

from selenium import webdriver


def open_linkedin(driver):
    def save_cookie(driver):
        pickle.dump(driver.get_cookies(), open("../cookies.pkl", "wb"))

    driver.get("https://www.linkedin.com/")
    print("Opened driver")
    input("Ready? input any string: ")

    save_cookie(driver)

    driver.get("https://www.linkedin.com/")
    print("Cookies are successfully saved.")


driver = webdriver.Firefox(executable_path='./geckodriver')
open_linkedin(driver)
