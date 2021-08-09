from os import link, name
from typing import final
from pandas.core.arrays.categorical import contains
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import html5lib
import requests
import pandas as pd
from pandas import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
import time
import re
from bs4 import BeautifulSoup, SoupStrainer

chrome_driver_path = '/Users/justinbenfit/Desktop/Python/chromedriver'
driver = webdriver.Chrome(executable_path=chrome_driver_path)

links_list = []
contact_list = []

test_links = ["https://www.servprocentralantelope.com/",'https://www.servproyavapaicounty.com/','https://www.servproyumaeastfoothills.com/','https://www.servpronorthernwestchestercounty.com/','https://www.servproanniston.com/','https://www.servprocalgarysouthab.com/','https://www.servproofbirmingham.com/']
contact_us_test_links = ['https://www.servproyavapaicounty.com/company-profile','https://www.servpronorthernwestchestercounty.com/company-profile','https://www.servprocalgarysouthab.com/company-profile','https://www.servproofbirmingham.com/company-profile']
last_test = ['https://www.servproyavapaicounty.com/contact/contactus','https://www.servpronorthernwestchestercounty.com/contact/contactus','https://www.servprocalgarysouthab.com/contact/contactus','https://www.servproofbirmingham.com/contact/contactus']

def get_links():

    url = 'https://www.servpro.com/sitemap/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'lxml')
    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        link = link.get('href')
        links_list.append(link)

def get_name(url):
    driver.get(url)
    url = driver.current_url
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'lxml')
    try:
        name = soup.find(class_="owner-photo col-sm-5").h2
    except AttributeError as a:
        print(a)
    else:
        return name

def get_website(url):
    driver.get(url)
    url = driver.current_url
    try:
        website = driver.current_url
    except AttributeError as a:
        print(a)
    else:
        return website

def get_phone(url):
    driver.get(url)
    url = driver.current_url
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'lxml')
    try:
        phone = soup.find('a', {'id': 'number_link'}).text
    except AttributeError as a:
        print(a)
    else:
        return phone

def get_email(url):
    driver.get(url)
    url = driver.current_url
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'lxml')
    try:
        email = soup.select_one("a[href*=mailto]").text
    except AttributeError as a:
        print(a)
        #print("No Email")
    else:
        return email

def get_address(url):
    driver.get(url)
    url = driver.current_url
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'lxml')
    try:
        address = soup.find("div",{"class": "col-sm-6 col-md-5"}).text
    except AttributeError as a:
        print(a)
    else:
        return address

def get_state(url):
    driver.get(url)
    url = driver.current_url
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'lxml')
    try:
        s1 = soup.find("div",{"class": "col-sm-6 col-md-5"}).text
        reversed_list = list(reversed(s1))[18:20]
        un_reversed = list(reversed(reversed_list))
        state = ''.join(un_reversed)
    except AttributeError as a:
        print(a)
    else:
        return state

def get_contact_us_page(url):
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    driver.get(url)
    try:
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.LINK_TEXT, "CONTACT US")))
    except TimeoutException:
        print("No Contact Us Page!")
        driver.quit()
    else:
        current_url = driver.current_url
        link_click = driver.find_element(By.LINK_TEXT, "CONTACT US")
        link_click.click()
        WebDriverWait(driver, 15).until(EC.url_changes(current_url))
        url = driver.current_url
        global email, address, state
        email = get_email(url)
        address = get_address(url)
        state = get_state(url)
        
def get_company_profile(url):
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    driver.get(url)
    try:
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.LINK_TEXT, "locally owned and operated")))
    except TimeoutException:
        print("No Company Profile Page!")
        driver.quit()
    else:
        current_url = driver.current_url
        link = driver.find_element(By.LINK_TEXT, "locally owned and operated")
        link.click()
        WebDriverWait(driver, 15).until(EC.url_changes(current_url))
        new_url = driver.current_url
        global name, phone, website
        name = get_name(new_url)
        phone = get_phone(new_url)
        website = get_website(new_url)
        get_contact_us_page(new_url)
        

def clean_dict(my_dict):
        my_dict = {k: v[0] for k, v in my_dict.items()}
        for k, v in my_dict.items():
            if '<h2>' in v:
                my_dict[k] = v.replace('<h2>', '').replace('</h2>', '')
        contact_list.append(my_dict)

def create_dict(url):
    get_company_profile(url)
    my_dict = {"Name":[],"Phone":[],"Email":[],"Website":[],"Address":[],"State":[]}
    my_dict["Name"].append(name)
    my_dict["Phone"].append(phone)
    my_dict["Email"].append(email)
    my_dict["Website"].append(website)
    my_dict["Address"].append(address)
    my_dict["State"].append(state)
    clean_dict(my_dict)

def test():
    for l in test_links:
        create_dict(l)
        
test()

def to_csv():
    pd.DataFrame(contact_list, dtype="string").to_csv("SERVPRO.csv")
to_csv()

driver.quit()



        


