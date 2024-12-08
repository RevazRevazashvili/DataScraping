from playwright.sync_api import sync_playwright
from seleniumbase import SB
import json
from bs4 import BeautifulSoup
import csv
import pandas as pd
import time
import requests
from selenium.webdriver.common.by import By

################# company raw links scraping ######################
links = []
proxy_string = "25f962c67d67a9a10edc__cr.us:358a70d297fbc821@gw.dataimpulse.com:823"
# with SB(uc=True, headless=False) as sb:
#     for page in range(1, 196):
#         sb.open(f"https://www.manta.com/search?search=Locks%20and%20Locksmiths&context=industry&search_source=nav&city=New%20York&state=New%20York&country=United%20States&pt=40.6943%2C-73.9249&device=desktop&screenResolution=1537x710&pg={page}")
#         sb.uc_gui_click_captcha()
#         try:
#             soup = BeautifulSoup(sb.get_page_source(), "html.parser")
#             raw_comp_links = soup.find_all("a", class_="cursor-pointer hover:text-primary-v1")
#             comp_links = ["https://www.manta.com"+link.get("href")+"\n" for link in raw_comp_links]
#             links.extend(comp_links)
#             print(f"scraped {page}-th page")
#         except:
#             continue
# with open("manta_comp_links1.txt", "a") as file:
#     file.writelines(links)


with open("manta_comp_links1.txt", "r") as file:
    links = set(file.readlines())

with SB(uc=True, headless=False, proxy=proxy_string) as sb:
    for link in links:
        sb.open(link.strip())
        sb.uc_gui_handle_captcha()
        loc, tel, web = [None]*3        
        new_row = {}
        try:
            loc = sb.find_element(By.CLASS_NAME, "pb-2 lg:pb-0 mr-6 hover:underline hidden lg:block").text
        except:
            pass
        try:
            tel = sb.find_element(By.CLASS_NAME, "pb-2 lg:pb-0 lg:mr-6").text
        except:
            pass
        try:
            raw_web = sb.find_element(By.CLASS_NAME, "pb-2 lg:pb-0 lg:mr-6 hidden lg:block text-gray-800")
            web = web.find_element(By.TAG_NAME, "a")
            web = web.get("href")
        except:
            pass
        print(loc, tel, web)


