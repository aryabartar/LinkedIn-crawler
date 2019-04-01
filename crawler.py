import time
import bs4 as bs
import csv
import glob

from random import randint
from utils import append_to_file, read_file, write_to_file, open_linkedin, scroll_to_button, \
    remove_first_and_last_spaces, make_dir


def random_wait():
    random = randint(2, 3)
    time.sleep(random)


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


def get_and_save_page_alumni_html(driver, url, file_path, slow_scroll=False):
    """This method will open, scroll and save html file of all alumni in univesity page"""
    driver.get(url)
    time.sleep(4)
    html = driver.page_source

    soup = bs.BeautifulSoup(html, 'lxml')
    alumni_number = soup.find('span', {"class": "t-20"}).text
    alumni_number = remove_first_and_last_spaces(alumni_number)

    scroll_number = int(int(alumni_number.split(' ')[0].replace(',', '')) / 12)
    print("Scroll Number: ", scroll_number, " |Alumni number: ", alumni_number)
    scroll_to_button(driver, scroll_number, slow_scroll)

    page_source = driver.page_source
    write_to_file(file_path, page_source.encode("utf-8"), is_binary=True)

    print("Saved alumni page to txt file.")
    return page_source


def write_name_and_link_list_to_csv(html_file_path):
    def get_name_and_links_array(path):
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
                name = remove_first_and_last_spaces(name)
                url = profile.find('a', class_='link-without-visited-state ember-view').get('href', None)
                url = make_url_complete(url)
                names_list.append({"name": name, "url": url})

        return names_list

    name_and_link_array = get_name_and_links_array(html_file_path)
    csv_file_path = html_file_path.replace("html", "csv")

    with open(csv_file_path, mode='w') as name_and_link_file:
        employee_writer = csv.writer(name_and_link_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for name_and_link in name_and_link_array:
            id = name_and_link["url"].split("/")[-2]
            employee_writer.writerow([id, name_and_link["name"], name_and_link["url"]])

    return csv_file_path


def get_and_save_profile_html(driver, link, write_to_address):
    """ Opens link page and saves FULL htm (with information in determined place."""
    link += "detail/contact-info/?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base%3BbOq%2BEFlwTxiy1KFi%2FKpHGw%3D%3D&licu=urn%3Ali%3Acontrol%3Ad_flagship3_profile_view_base-contact_see_more"
    driver.get(link)
    scroll_to_button(driver, 2)
    time.sleep(randint(5, 10))  # For loading entire website (skills and experience)
    page_source = driver.page_source
    if "Join to view full profiles for free" in page_source:
        raise Exception("Logged out. Please login.")
    write_to_file(write_to_address, page_source.encode("utf-8"), is_binary=True)


def get_and_save_people_information_to_csv(dir, csv_path):
    if not dir[-1] == "/":
        dir = dir + "/"

    htmls_path_list = glob.glob(dir + "*.aryatml")

    with open(csv_path, mode='w') as profile_info_file:
        profile_info_writer = csv.writer(profile_info_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        first_row = True

        for path in htmls_path_list:
            info_dict = get_person_information(path)

            if info_dict.get('id', None) is None:
                continue

            if first_row:
                profile_info_writer.writerow(list(info_dict.keys()))
                first_row = False
            profile_info_writer.writerow(list(info_dict.values()))

        profile_info_file.close()


def get_person_information(html_path):
    def make_phone_pretty(phone):
        phone = remove_first_and_last_spaces(phone)
        return phone

    def make_name_pretty(name):
        name = remove_first_and_last_spaces(name)
        return name

    def make_email_pretty(email):
        email = remove_first_and_last_spaces(email)
        return email

    def get_name(soup):
        name = None
        try:
            name = soup.find('h1', {"id": "pv-contact-info"}).text
            name = remove_first_and_last_spaces(name)
        except:
            name = None
        return name

    def get_profile_url(soup):
        profile_url = None
        try:
            profile_url_html = soup.find('a', {"class": "pv-contact-info__contact-link"})
            profile_url = profile_url_html.get('href')
        except:
            profile_url = None

        return profile_url

    def get_id(soup):
        id = None
        try:
            id = profile_url.split("/")[-1]
        except:
            id = None
        return id

    def get_email(soup):
        email = None
        try:
            section_html = soup.find('section', class_='ci-email')
            email = section_html.find('a', class_='pv-contact-info__contact-link').text
            email = make_email_pretty(email)
        except:
            email = None
        return email

    def get_phone(soup):
        phone = None
        try:
            section_html = soup.find('section', class_='ci-phone')
            phone = section_html.find('span', class_='t-black').text
            phone = make_phone_pretty(phone)
        except:
            phone = None
        return phone

    def get_websites(soup):
        websites = None
        try:
            section_html = soup.find('section', class_='ci-websites')
            websites_html = section_html.find_all('a', class_='pv-contact-info__contact-link')

            websites = []
            for website_html in websites_html:
                websites.append(str(website_html.get('href')))
        except:
            websites = None
        return websites

    def get_universities(soup):
        universities = None
        try:
            university_section_html = soup.find('section', class_='education-section')
            universities_html = university_section_html.find_all('li', class_='pv-profile-section__sortable-item')
            universities = []
            for university in universities_html:
                temp_str = ""

                university_name = university.find('h3', class_='pv-entity__school-name').text
                temp_str = temp_str + "University name: " + remove_first_and_last_spaces(university_name) + " || "

                try:
                    degree = university.find('p', class_='pv-entity__secondary-title').find('span',
                                                                                            class_='pv-entity__comma-item').text
                    temp_str += "Degree: " + remove_first_and_last_spaces(degree) + " || "
                except:
                    pass

                try:
                    field_of_study = university.find('p', class_='pv-entity__fos').find('span',
                                                                                        class_='pv-entity__comma-item').text
                    temp_str += "Field Of Study: " + remove_first_and_last_spaces(field_of_study) + " || "
                except:
                    pass

                date_str = None
                try:
                    dates = soup.find('p', class_='pv-entity__dates').find_all('time')
                    temp_str += "Date: " + dates[0].text + "-" + dates[1].text.replace("'", "")
                except:
                    pass

                universities.append(temp_str)
        except:
            universities = None
        return universities

    def get_skills(soup):
        # 3 top skills
        skills = None
        try:
            skills_html = soup.find_all('span', class_='pv-skill-category-entity__name-text')
            skills = []
            for skill in skills_html:
                skills.append(remove_first_and_last_spaces(skill.text))
        except:
            skills = None
        return skills

    def get_experiences(soup):
        experiences = None
        try:
            experience_section_html = soup.find('section', class_='experience-section')
            experiences_html = experience_section_html.find_all('div', class_='pv-entity__position-group-pager')
            experiences = []

            for experience_html in experiences_html:
                temp_experience_str = ""
                title = experience_html.find('h3', {'class': ['t-16', 't-black', 't-bold']}).text
                company_name = experience_html.find('h4', {'class': ['t-16', 't-black', 't-normal']}).text

                company_name_array = company_name.split("\n")
                if not company_name_array[1] == 'Company Name':
                    raise Exception("Invalid company format!")

                company_name = company_name_array[2]
                temp_experience_str = "Title: " + title + " | Company: " + company_name
                experiences.append(temp_experience_str)
        except:
            pass

        return experiences

    html = read_file(html_path)
    soup = bs.BeautifulSoup(html, 'lxml')

    name = get_name(soup)
    profile_url = get_profile_url(soup)
    id = get_id(soup)
    phone = get_phone(soup)
    email = get_email(soup)
    websites = get_websites(soup)
    universities = get_universities(soup)
    skills = get_skills(soup)
    experiences = get_experiences(soup)

    information_dict = {
        "id": id,
        "name": name,
        "profile_url": profile_url,
        "email": email,
        "phone": phone,
        "websites": websites,
        "skills": skills,
        "universities": universities,
        "experiences": experiences,
    }

    return information_dict


def get_and_save_profiles_html(csv_path, save_folder_path, driver):
    profiles = []
    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            try:
                profiles.append({"id": row[0], "name": row[1], "url": row[2]})
            except:
                # When row is empty(When all members are not connectible)
                pass

        for profile in profiles:

            fetch_list_file_path = save_folder_path + "/html-fetch-log.txt"

            try:
                fetched_profiles_id = read_file(fetch_list_file_path).split("||")
                if profile["id"] not in fetched_profiles_id:
                    random_wait()
                    get_and_save_profile_html(driver, profile["url"],
                                              save_folder_path + "/" + profile["id"] + ".aryatml")
                    append_to_file(fetch_list_file_path, "||" + profile["id"])
                    print("Successfully saved profile html.")

                else:
                    print("Profile html exists. still running ...")
            except:
                print("An error occurred while saving profile html but still running ...")


def get_text_information_from_html(dir_path):
    """Used to extract raw data from all dir_path subdirectory html files. """
    dirs_list = glob.glob(dir_path + "/*/")

    for dir in dirs_list:
        htmls_path_list = glob.glob(dir + "*.html")

        for html_path in htmls_path_list:
            html = read_file(html_path)
            soup = bs.BeautifulSoup(html, 'lxml')
            raw_text = soup.text
            text_path = html_path.replace(".html", ".txt")
            raw_text = raw_text.replace("\n", "")
            write_to_file(text_path, raw_text, is_binary=True)


mode = input("Choose mode (1, 2, 3, 4): ")
dr_name = input("Input directory name: ")
main_dir_path = "../app-data/crawler/alumni/" + dr_name
primary_data_path = main_dir_path + "/primary"

make_dir(main_dir_path)
make_dir(primary_data_path)

if mode == '1':
    driver = open_linkedin()
    url = input("Input alumni url: ")
    amirkabir_alumni_html = get_and_save_page_alumni_html(driver, url, primary_data_path + "/alumni_html.html")
    csv_file_path = write_name_and_link_list_to_csv(primary_data_path + "/alumni_html.html")
    get_and_save_profiles_html(csv_file_path, main_dir_path, driver)
    get_and_save_people_information_to_csv(main_dir_path, primary_data_path + "/FINAL.csv")

elif mode == '2':
    driver = open_linkedin()
    get_and_save_profiles_html(primary_data_path + "/alumni_csv.csv", main_dir_path, driver)

elif mode == '3':
    get_and_save_people_information_to_csv(main_dir_path, primary_data_path + "/FINAL.csv")

elif mode == '4':
    url = input("Input alumni url: ")
    driver = open_linkedin()
    get_and_save_page_alumni_html(driver, url, primary_data_path + "/alumni_html.html")
    write_name_and_link_list_to_csv(primary_data_path + "/alumni_html.html")

print("Done")
