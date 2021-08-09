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
url2_links = []
contact_list = []

test_links = ['https://www.servproyavapaicounty.com/contact/contactus','https://www.servproyumaeastfoothills.com/','https://www.servpronorthernwestchestercounty.com/','https://www.servproanniston.com/','https://www.servprocalgarysouthab.com/company-profile','https://www.servproofbirmingham.com/']

def get_links():
    url = 'https://www.servpro.com/sitemap/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'lxml')
    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        link = link.get('href')
        links_list.append(link)
#get_links()
#print(links_list)
#df = pd.DataFrame(links_list).to_csv("Links.csv")



def get_local_page():
    while True:
        try:
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.LINK_TEXT, "locally owned and operated")))
            link_click = driver.find_element(By.LINK_TEXT, "locally owned and operated")
            link_click.click()
            break
        except TimeoutError as t:
            print(t)
            break
    

def get_contact_us_page():
    while True:
        try:
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.LINK_TEXT, "CONTACT US")))
            link_click = driver.find_element(By.LINK_TEXT, "CONTACT US")
            link_click.click()
            break
        except TimeoutError as t:
            print(t)
            break


def setup(url1):
    while True:
        try:
            driver.get(url1)
            time.sleep(1)
            get_local_page()
            url2 = driver.current_url
            page = requests.get(url2)
            print(page)
            soup = BeautifulSoup(page.content,'lxml')
            return soup
        except TimeoutException:
            print("content not present")
            break

setup("https://www.servprocentralantelope.com/")

def get_name(url1):
    soup = setup(url1)
    try:
        name = soup.find(class_="owner-photo col-sm-5").h2
        return str(name)
    except Exception:
        return "No Name"
        

def get_phone(url1):
    soup = setup(url1)
    try:
        phone_number = soup.find('a', {'id': 'number_link'}).text
        return phone_number
    except Exception:
        return "No Phone"
        

def get_website(url1):
    try:
        driver.get(url1)
        time.sleep(1)
        get_local_page()
        website = driver.current_url
        return str(website)
    except TimeoutException:
        return

def setup_contact_us(url1):
    while True:
        try:
            setup(url1)
            get_contact_us_page()
            url3 = driver.current_url
            page1 = requests.get(url3)
            soup1 = BeautifulSoup(page1.content,'lxml')
            return soup1
        except TimeoutException:
            break

def get_email(url1):
    soup = setup_contact_us(url1)
    try:
        email = soup.select_one("a[href*=mailto]").text
        return email
    except Exception:
        return "No Email"
        

def get_address(url1):
    soup = setup_contact_us(url1)
    try:
        address = soup.find("div",{"class": "col-sm-6 col-md-5"}).text
        return address
    except Exception:
        return "No Address"
        

def get_state(url1):
    soup = setup_contact_us(url1)
    try:
        s1 = soup.find("div",{"class": "col-sm-6 col-md-5"}).text
        reversed_list = list(reversed(s1))[18:20]
        un_reversed = list(reversed(reversed_list))
        state = ''.join(un_reversed)
        return state
    except Exception:
        return "No State"
        

#get_phone('https://www.servpronorthernwestchestercounty.com/')
#get_email('https://www.servprocalgarysouthab.com/company-profile')
#get_address('https://www.servpronorthernwestchestercounty.com/')
#get_state('https://www.servpronorthernwestchestercounty.com/')
#get_website('https://www.servpronorthernwestchestercounty.com/')

def clean_dict(my_dict):
        my_dict = {k: v[0] for k, v in my_dict.items()}
        for k, v in my_dict.items():
            if '<h2>' in v:
                my_dict[k] = v.replace('<h2>', '').replace('</h2>', '')
        contact_list.append(my_dict)
        
        
def create_dict(url):
    name = get_name(url)
    phone = get_phone(url)
    email = get_email(url)
    website = get_website(url)
    address = get_address(url)
    state = get_state(url)
    my_dict = {"Name":[],"Phone":[],"Email":[],"Website":[],"Address":[],"State":[]}
    my_dict["Name"].append(name)
    my_dict["Phone"].append(phone)
    my_dict["Email"].append(email)
    my_dict["Website"].append(website)
    my_dict["Address"].append(address)
    my_dict["State"].append(state)
    clean_dict(my_dict)
    
    
def loop_urls1():
    get_links()
    for l in links_list[2:113]:
        create_dict(l)
    pass
    
    

def loop_urls2():
    get_links()
    for l in links_list[117:141]:
        create_dict(l)
    pass

def loop_urls3():
    get_links()
    for l in links_list[144:]:
        create_dict(l)
    pass
        
#loop_urls1()
#time.sleep(3)
#loop_urls2()
#time.sleep(3)
#loop_urls3()

def to_csv():
    df = pd.DataFrame(contact_list, dtype="string")
    df.to_csv("SERVPRO.csv")
#o_csv()   
driver.quit() 

