import time
import pickle

from random import randint
from selenium import webdriver

SPECIAL_CHARACTER = "/|||\\"  # This special notation is used to replace given characters


def write_to_file(path, text):
    f = open(path, "w")
    f.write(text)
    f.close()


def read_file(path):
    f = open(path, "r")
    text = f.read()
    f.close()
    return text


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
    # restore_cookie(driver)
    # time.sleep(100)
    restore_cookie(driver)
    driver.get("https://www.linkedin.com/")


def get_amirkabir_alumni_html(driver):
    aut_usa_url = "https://www.linkedin.com/school/amirkabir-university-of-technology---tehran-polytechnic/people/?facetGeoRegion=us%3A0"
    driver.get(aut_usa_url)
    page_resource = driver.page_source
    f = open("alumni-htmls/Amirkabir.html", "w")
    f.write(page_resource)
    f.close()
    return page_resource


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


def get_and_save_profile_html(driver, link):
    """ Opens link page and saves FULL htm (with information in determined place."""
    link += "detail/contact-info/?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base%3BbOq%2BEFlwTxiy1KFi%2FKpHGw%3D%3D&licu=urn%3Ali%3Acontrol%3Ad_flagship3_profile_view_base-contact_see_more"
    driver.get(link)
    page_source = driver.page_source

    html_address = "people-htmls/test.html"
    write_to_file("people-htmls/test.html", page_source)

    return html_address


def get_person_information(html_path):
    def remove_first_spaces(text):
        # removes name spaces
        i = 0
        for i in range(0, len(text)):
            if text[i] != " ":
                break
        text = text[i:]
        return text

    def make_name_pretty(name):
        name = remove_first_spaces(name)
        return name

    def make_email_pretty(email):
        email = remove_first_spaces(email)
        return email

    html = read_file(html_path)
    html = html.replace(">", SPECIAL_CHARACTER)
    html = html.replace("<", SPECIAL_CHARACTER)
    html = html.replace("\n", SPECIAL_CHARACTER)

    html = html.replace('h1 class="pv-top-card-section__name inline t-24 t-black t-normal"', "craw_person_name")
    html = html.replace(
        'a href="mailto:nastaranour73@gmail.com" class="pv-contact-info__contact-link t-14 t-black t-normal" target="_blank" rel="noopener noreferrer"',
        "craw_person_email")

    html_array = html.split(SPECIAL_CHARACTER)

    name_temp_index = html_array.index('craw_person_name')
    name = html_array[name_temp_index + 2]
    name = make_name_pretty(name)

    email_temp_index = html_array.index('craw_person_email')
    email = html_array[email_temp_index + 2]
    email = make_email_pretty(email)

    print(email)

# driver = webdriver.Firefox()
# open_linkedin(driver)
# random_wait()
# amirkabir_alumni_html = get_amirkabir_alumni_html(driver)
# print(find_names_from_main_page(amirkabir_alumni_html))
# get_and_save_profile_html(driver,
#                           "https://www.linkedin.com/in/nastaran-nourbakhsh-860a6216b/")

get_person_information("people-htmls/test.html")
