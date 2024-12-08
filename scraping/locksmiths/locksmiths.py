import time
from typing import Dict, List

from seleniumbase import SB
from bs4 import BeautifulSoup, ResultSet, Tag
import pandas as pd

proxy_string = "25f962c67d67a9a10edc:358a70d297fbc821@gw.dataimpulse.com:823"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}
info = pd.read_csv("output2.csv")
links = info['textbluemedium_URL'].tolist()


def scrape_company(link: str) -> dict[str, str | None | list[str] | ResultSet[Tag]]:
    with SB(uc=True, proxy=proxy_string, headless=True) as sb:
        sb.open(link)
        time.sleep(3)  # Allow time for the page to load fully
        page_source = sb.get_page_source()
        soup = BeautifulSoup(page_source, "html.parser")

        # Initialize variables
        name, loc, mob, owners, web = [None] * 5

        # Extract company name
        try:
            name_element = soup.find("span", class_="bds-h2 font-normal text-black")
            if name_element:
                name = name_element.get_text(strip=True)
        except Exception as e:
            print("Error extracting company name:", e)

        # Extract company location
        try:
            loc_element = soup.select_one(
                "#content > div.page-center.stack.stack-space-24 > div.profile-at-a-glance.with-sidebar.gutter-24 > div.sidebar > div > div.dtm-address.with-icon > div > address"
            )
            if loc_element:
                loc = loc_element.get_text(strip=True)
        except Exception as e:
            print("Error extracting location:", e)

        # Extract phone number
        try:
            mob_element = soup.find("a", class_="dtm-phone")
            if mob_element:
                mob = mob_element.get_text(strip=True)
        except Exception as e:
            print("Error extracting phone number:", e)

        # Extract owner names
        try:
            owners_elements = soup.select(
                "dd>ul.list-reset:only-child"
            )
            if owners_elements:
                owners = owners_elements[-1].get_text()
        except Exception as e:
            print("Error extracting owners:", e)
        try:
            web = soup.select(
                "a.dtm-url"
            )
            if web:
                web = web[0].get("href")
        except Exception as e:
            print("Error extracting owners:", e)
        row = {
            "Name:": name,
            "Location:": loc,
            "Phone Number:": mob,
            "Owners:": owners,
            "Website:": web
        }
        return row
df = pd.DataFrame(["Name:", "Location:", "Phone Number:", "Owners:", "Website:"])
for link in links:
    try:
        print(f"processing {link}")
        row = scrape_company(link.strip())
        if row:
            df.loc[len(df)] = row
            print(row)
    except:
        continue
df.to_csv("info.csv")