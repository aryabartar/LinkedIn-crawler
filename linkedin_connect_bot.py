import time
import bs4 as bs

from random import randint
from utils import append_to_file, read_file, open_linkedin


def random_wait():
    random = randint(3, 4)
    time.sleep(random)


def connect_to_alumni(page_url, save_ids_path, driver):
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

    def connected_before(file_path, id):
        ids_list = read_file(file_path).split("||")
        if id in ids_list:
            return True
        return False

    def get_profile_id(profile_html):
        profile_link = profile_html.find('a', {"class": "link-without-visited-state"}).get('href')
        profile_id = profile_link.split("/")[-2]
        return profile_id

    driver.get(page_url)
    random_wait()

    html = driver.page_source
    soup = bs.BeautifulSoup(html, 'lxml')

    alumni_number = soup.find('span', {"class": "t-20"}).text
    alumni_number = remove_first_and_last_spaces(alumni_number)
    scroll_number = int(int(alumni_number.split(' ')[0]) / 12)
    print("Scroll Number: ", scroll_number, " |Alumni number: ", alumni_number)

    scroll_to_button(scroll_number)
    random_wait()

    html = driver.page_source
    soup = bs.BeautifulSoup(html, 'lxml')

    people_html = soup.find_all('li', {"class": "org-people-profiles-module__profile-item"})
    people_number = len(people_html)

    for i in range(0, people_number - 1):
        try:

            try:
                # Notification when connecting much.
                driver.find_element_by_class_name('ip-fuse-limit-alert__primary-action').click()
                print("Clicked on notification button. ")
            except:
                pass

            profile_id = get_profile_id(people_html[i])
            if connected_before(save_ids_path, profile_id):
                continue
            else:
                append_to_file(save_ids_path, "||{profile_id}".format(profile_id=profile_id))

            # Click on connect button
            driver.find_element_by_xpath(
                '/html/body/div[5]/div[6]/div[2]/div/div[2]/div/main/div[2]/ul/li[{id}]/div/ul/li/button'.format(
                    id=i + 1)).click()

            time.sleep(1)

            # Click on ok button
            driver.find_element_by_xpath(
                '/html/body/div[5]/div[7]/div/div[1]/div/section/div/div[2]/button[2]').click()

            time.sleep(1)
            print("connected")

        except Exception as e:
            print("Error while connecting.")

    random_wait()


driver = open_linkedin()
connect_to_alumni(
    'https://www.linkedin.com/school/amirkabir-university-of-technology---tehran-polytechnic/people/?facetGeoRegion=ca%3A0&keywords=turkey',
    '../linkedin_connect_bot_data/turkey.txt',
    driver)
