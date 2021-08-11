from os import link, name
from numpy.testing._private.utils import IgnoreException
from pandas.core.arrays.categorical import contains
from requests.api import get
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import html5lib
import requests
import pandas as pd
from pandas import *
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, WebDriverException
from selenium.common.exceptions import NoSuchElementException
import time
import re
from selenium.webdriver.chrome.options import Options

# url = "https://www.servprocentralantelope.com/"

test_links = ['https://www.servpronorthtempe.com/', 'https://www.servproyumaeastfoothills.com/',
              'https://www.servpronorthernwestchestercounty.com/', 'https://www.servproanniston.com/', 'https://www.servprocalgarysouthab.com/', 'https://www.servproofbirmingham.com/']
contact_us_test_links = ['https://www.servproyavapaicounty.com/company-profile', 'https://www.servpronorthernwestchestercounty.com/company-profile',
                         'https://www.servprocalgarysouthab.com/company-profile', 'https://www.servproofbirmingham.com/company-profile']
last_test = ['https://www.servproyavapaicounty.com/contact/contactus', 'https://www.servpronorthernwestchestercounty.com/contact/contactus',
             'https://www.servprocalgarysouthab.com/contact/contactus', 'https://www.servproofbirmingham.com/contact/contactus']

links_list = []


def get_links(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        link = link.get('href')
        links_list.append(link)


contact_list = []
no_company_or_contact = []

chrome_driver_path = '/Users/Justin/Desktop/Python/chromedriver'
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument("--start-maximized")


def get_name_phone_website(driver, url):
    my_dict = {"Name": [], "Phone": [], "Website": []}
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    try:
        name = soup.find(class_="owner-photo col-sm-5").h2
    except AttributeError as a:
        print(f"{a} in name for {url}")
        my_dict["Name"].append("No Name")
    else:
        my_dict["Name"].append(str(name))
    try:
        phone = soup.find('a', {'id': 'number_link'}).text
        website = driver.current_url
    except AttributeError as a:
        print(f"{a} in phone or website for {url}")
        my_dict["Website"].append("No Website")
        my_dict["Phone"].append("No Phone")
        return my_dict
    else:
        my_dict["Website"].append(website)
        my_dict["Phone"].append(phone)
    return my_dict


def get_email_address_state(url):
    my_dict = {"Email": [], "Address": [], "State": []}
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    try:
        email = soup.select_one("a[href*=mailto]").text
    except AttributeError as a:
        print(f"{a} in email for {url}")
        my_dict["Email"].append("No Email")
    else:
        my_dict["Email"].append(email)
    try:
        address = soup.find("div", {"class": "col-sm-6 col-md-5"}).text
        s1 = soup.find("div", {"class": "col-sm-6 col-md-5"}).text
        reversed_list = list(reversed(s1))[18:20]
        un_reversed = list(reversed(reversed_list))
        state = ''.join(un_reversed)
    except AttributeError as a:
        print(f"{a} in address for {url}")
        my_dict["Address"].append("No Address")
        my_dict["State"].append("No State")
    else:
        my_dict["Address"].append(address)
        my_dict["State"].append(state)
    return my_dict


def merge(dict1, dict2):
    ignored_errors = TypeError, AttributeError
    try:
        res = {**dict1, **dict2}
    except ignored_errors as t:
        print(f"{t} in merged_dict for {url}")
        return
    else:
        return res


def clean_dict(my_dict):
    try:
        my_dict = {k: v[0] for k, v in my_dict.items()}
        for k, v in my_dict.items():
            if v is not None and '<h2>' in v:
                my_dict[k] = v.replace('<h2>', '').replace('</h2>', '')

    except AttributeError as a:
        print(f"{a} in clean_dict for {url}")
        return
    else:
        contact_list.append(my_dict)


def test_pop_up(driver, url):
    try:
        time.sleep(3)
        link_click = driver.find_element(By.LINK_TEXT, "CONTACT US")
        link_click.click()
        WebDriverWait(driver, 15).until(EC.url_changes(url))
        url = driver.current_url
    except NoSuchElementException as n:
        #print(f"{n} in test_pop for {url}")
        iframe = driver.find_element_by_xpath(
            "//iframe[contains(@id,'zychatObject')]")
        driver.switch_to.frame(iframe)
        close_pop_up = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@id='closeChat']")))
        close_pop_up.click()
        driver.switch_to.default_content()
        link_click = driver.find_element(By.LINK_TEXT, "CONTACT US")
        link_click.click()
        WebDriverWait(driver, 15).until(EC.url_changes(url))
        url = driver.current_url
        return url
    else:
        return url


def get_contact_us_page(driver, url):
    ignored_exceptions = TimeoutException, NoSuchElementException
    try:
        contact_us_url = test_pop_up(driver, url)
    except ignored_exceptions:
        no_company_or_contact.append(f"No Contact Us Page for {url}!")
    else:
        my_dict2 = get_email_address_state(contact_us_url)
        return my_dict2
        # print(my_dict2)


# get_contact_us_page('https://www.servproanniston.com/company-profile')

def get_company_profile(driver, url):
    try:
        driver.get(url)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.LINK_TEXT, "locally owned and operated")))
    except TimeoutException as t:
        print(f"{t} in company profile for {url}")
        no_company_or_contact.append(f"No Company Profile Page for {url}!")
        my_dict2 = get_contact_us_page(driver, url)
        print(f"{my_dict2} of {url}")
    else:
        current_url = driver.current_url
        link = driver.find_element(By.LINK_TEXT, "locally owned and operated")
        link.click()
        WebDriverWait(driver, 15).until(EC.url_changes(current_url))
        new_url = driver.current_url
        my_dict1 = get_name_phone_website(driver, new_url)
        my_dict2 = get_contact_us_page(driver, new_url)
        merged_dict = merge(my_dict1, my_dict2)
        clean_dict(merged_dict)
        return
        # print(my_dict1)
        # print(my_dict2)


url = 'https://www.servpro.com/sitemap/'


def master_func(url):
    get_links(url)
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    driver.get(url)
    loop = True
    for l in links_list:
        try:
            get_company_profile(driver, l)
        except WebDriverException:
            print("Connection Timed Out for {url}")
            return
        else:
            continue
        finally:
            if len(l) < 0:
                driver.quit()


master_func(url)


def to_csv():
    pd.DataFrame(contact_list, columns=[
                 "Name", "Phone", "Website", "Email", "Address", "State"], dtype="string").to_csv("SERVPRO.csv")
    pd.DataFrame(no_company_or_contact, dtype="string").to_csv(
        "No_Name_Contact_List.csv")


to_csv()
