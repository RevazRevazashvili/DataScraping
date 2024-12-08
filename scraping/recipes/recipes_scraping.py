import time
from typing import Dict, List
from seleniumbase import SB
from bs4 import BeautifulSoup
import pandas as pd
import json
import csv

proxy_string = "25f962c67d67a9a10edc:358a70d297fbc821@gw.dataimpulse.com:823" # proxy service
df = pd.read_csv("Timings - Sheet1.csv") #provided links file
urls = df['URL']

columns = [
    "url", "name", "prepTime", "cookTime", "totalTime"
]
# Create output CSV file
with open("recipes1.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()

with SB(uc=True, proxy=proxy_string, headless=False, ad_block=True) as sb:
    for url in urls:
        try:
            sb.open(url)
            time.sleep(2)
            page_source = sb.get_page_source()
            soup = BeautifulSoup(page_source, "html.parser")
            try:
                script_tag = soup.find_all('script', type='application/ld+json')[1]
                if script_tag:
                    recipe_data = json.loads(script_tag.string)
                    new_row = {
                        "url": url,
                        "name": recipe_data.get('name', "N/A"),
                        "prepTime": recipe_data.get('prepTime', "N/A"),
                        "cookTime": recipe_data.get('cookTime', "N/A"),
                        "totalTime": recipe_data.get('totalTime', "N/A")
                    }
                    with open("recipes1.csv", "a", newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=columns)
                        writer.writerow(new_row)
                        print(new_row)
                else:
                    print(f"No JSON-LD script found for URL: {url}")
            except Exception as e:
                with open("errors.txt","a")as f:
                    f.write(url+"\n")
                print(f"Error processing {url}: {e}")

        except Exception as e:
            print(f"Error scraping {url}: {e}")

