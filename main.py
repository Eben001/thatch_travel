import os
import re
import random
import asyncio
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from utils import *
import csv
import requests
import signal
import pandas as pd
from random import randint
import time


from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
ua = UserAgent()

from requests_html import AsyncHTMLSession
import asyncio
if asyncio.get_event_loop().is_running():
    import nest_asyncio
    nest_asyncio.apply()


base_url = 'https://www.thatch.co'

async def fetch_with_retry(url, max_retries=100, retry_delay=5):
    for attempt in range(max_retries):


      proxies={
        "http": "http://ywciwoyn-rotate:jjvehm8bwfvv@p.webshare.io:80/",
        "https": "http://ywciwoyn-rotate:jjvehm8bwfvv@p.webshare.io:80/"
        }

      session = AsyncHTMLSession(browser_args=["--no-sandbox", f'--user-agent={ua.random}'])

      response = await session.get(url)
      if response.status_code == 200:
        await response.html.arender(sleep=2,timeout=60)
        html_content = response.html.html
        return html_content

      print(f"Error {response.status_code}, Retrying: {attempt+1}, {url}")
      time.sleep(retry_delay)


async def main():
    global data_list
    try:
        total_pages = 270
        page_base = 'https://www.thatch.co/sellers/all'
        start_page = 118
        end_page = 150 
        page_urls = [f'{page_base}?page={page}' for page in range(start_page, end_page + 1)]


        # with ThreadPoolExecutor(max_workers=10) as executor:
        #     futures = []
        for page_link in page_urls:
          print(f"Currently scraping {page_link}")
          html_content = await fetch_with_retry(url=page_link)
          soup = BeautifulSoup(html_content, 'lxml')
          all_sellers = soup.find_all('div', class_='mantine-2ysq6o')
          print(len(all_sellers))
          for seller in all_sellers:
              try:
                name = seller.find('div', class_='mantine-Text-root mantine-1robxym').text
              except:
                name = ""

              try:
                link = seller.find('a', class_='mantine-Text-root mantine-Anchor-root mantine-1ceev6n')['href']
                full_link = base_url+link
              except:
                link = ""

              try:
                photo_url = seller.find('img', class_='mantine-1azyrim mantine-Image-image')['src']
              except:
                photo_url = ""
              try:
                bio = seller.find('div', class_='mantine-Text-root mantine-azy3d3').text
              except:
                bio = ""
              try:
                focuses = seller.find('div', class_='mantine-Text-root mantine-134x5qe').text
              except:
                focuses = ""
                
              await parse_sellers_details(full_link, name, photo_url, bio,focuses)
          
    except KeyboardInterrupt:
        print("Received KeyboardInterrupt. Stopping gracefully.")
    except Exception as e:
        print(f"Error while trying to find the seller item element: {str(e)}")
    finally:
        global_df = pd.DataFrame(data_list)
        global_df.to_excel('thatch_travel.xlsx', engine='xlsxwriter', index=False)


if __name__ == "__main__":
    asyncio.run(main())
    # main()