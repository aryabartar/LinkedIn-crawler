import time
import pickle
import bs4 as bs

from random import randint
from selenium import webdriver

SPECIAL_CHARACTER = "/|||\\"  # This special notation is used to replace given characters


def find_index_in_array(array, search_text):
    for element in array:
        if search_text in element:
            return array.index(element)
    return None


def find_number_of_repeats(array, search_text):
    count = 0
    indexes = []
    for i in range(0, len(array)):
        if search_text in array[i]:
            count += 1
            indexes.append(i)

    return count, indexes


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


def get_amirkabir_alumni_html(driver, file_name):
    aut_usa_url = "https://www.linkedin.com/school/amirkabir-university-of-technology---tehran-polytechnic/people/?facetGeoRegion=us%3A0"
    driver.get(aut_usa_url)
    finished = input("Finished crawling?")
    if finished == "True":
        page_resource = driver.page_source
        f = open("alumni-htmls/" + file_name, "w")
        f.write(page_resource)
        f.close()
        return page_resource


def find_names_from_main_page(path):
    def make_name_pretty(name):
        name = name.replace("\n", " ")
        for i in range(0, len(name)):
            if name[i] != ' ':
                break
        name = name[i:]
        for i in range(len(name) - 1, 0, -1):
            if name[i] != ' ':
                break
        name = name[: i + 1]
        return name

    def make_url_complete(url):
        url = "https://www.linkedin.com" + url
        return url

    names_list = []
    html = read_file(path)
    soup = bs.BeautifulSoup(html, 'lxml')

    profiles = soup.find_all('li', class_='org-people-profiles-module__profile-item')
    for profile in profiles:
        name_html = profile.find('div', class_='org-people-profile-card__profile-title')
        # When not showing 'LinkedIn Member'
        if name_html is not None:
            name = name_html.text
            name = make_name_pretty(name)
            url = profile.find('a', class_='link-without-visited-state ember-view').get('href', None)
            url = make_url_complete(url)
            names_list.append((name, url))

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

    def make_website_pretty(website):
        website = remove_first_spaces(website)
        i = 0
        for i in range(0, len(website)):
            if website[i] == "&":
                break

        return website[:i]

    def make_phone_pretty(phone):
        phone = remove_first_spaces(phone)
        return phone

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

    html_array = html.split(SPECIAL_CHARACTER)

    name_temp_index = find_index_in_array(html_array,
                                          'h1 class="pv-top-card-section__name inline t-24 t-black t-normal')
    name = html_array[name_temp_index + 2]
    name = make_name_pretty(name)

    try:
        email_temp_index = find_index_in_array(html_array,
                                               'class="pv-contact-info__contact-link t-14 t-black t-normal" target="_blank" rel="noopener noreferrer"')
        email = html_array[email_temp_index + 2]
        email = make_email_pretty(email)
    except:
        email = None

    try:
        phone_temp_index = find_index_in_array(html_array,
                                               'span class="t-14 t-black t-normal"')
        phone = html_array[phone_temp_index + 1]
        phone = make_phone_pretty(phone)
    except:
        phone = None

    try:
        website_temp_index = find_index_in_array(html_array,
                                                 'class="pv-contact-info__contact-link t-14 t-black t-normal" target="_blank" rel="noopener"')
        website = html_array[website_temp_index + 2]
        website = make_website_pretty(website)
    except:
        website = None

    try:
        universities = []
        university_count, university_temp_indexes = find_number_of_repeats(html_array,
                                                                           'pv-entity__school-name t-16 t-black t-bold')
        degree_repeat, degree_repeat_temp_indexes = find_number_of_repeats(html_array,
                                                                           'pv-entity__secondary-title pv-entity__degree-name pv-entity__secondary-title t-14 t-black t-normal')
        field_of_study_repeat, field_of_study_temp_indexes = find_number_of_repeats(html_array,
                                                                                    'pv-entity__secondary-title pv-entity__fos pv-entity__secondary-title t-14 t-black--light t-normal')
        if university_count == degree_repeat == field_of_study_repeat:
            for i in range(0, university_count):
                university = remove_first_spaces(html_array[university_temp_indexes[i] + 1])
                degree = remove_first_spaces(html_array[degree_repeat_temp_indexes[i] + 9])
                field = remove_first_spaces(html_array[field_of_study_temp_indexes[i] + 9])
                university_string = "University: " + university + "| Degree: " + degree + "| Field: " + field
                universities.append(university_string)

        else:
            for i in range(0, university_count):
                university = remove_first_spaces(html_array[university_temp_indexes[i] + 1])
                university_string = "University: " + university
                universities.append(university_string)

    except:
        pass

    print(name, " | ", email, " | ", phone, " | ", website, " | ", universities)


# driver = webdriver.Firefox()
# open_linkedin(driver)
# random_wait()
# amirkabir_alumni_html = get_amirkabir_alumni_html(driver, "temp.html")
print(find_names_from_main_page("alumni-htmls/amirkabir-Greater New York City Area.html"))
# get_and_save_profile_html(driver,
#                           "https://www.linkedin.com/in/soheil-tabatabaei-mortazavi-67a29259/")

# get_person_information("people-htmls/test.html")
