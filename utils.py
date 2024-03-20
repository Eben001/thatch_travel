import os
import time
import requests
from fake_useragent import UserAgent
from requests_html import AsyncHTMLSession
import json
from bs4 import BeautifulSoup
ua = UserAgent()

data_list = []


def get_current_directory_path(filename):
    return os.path.join(os.getcwd(), filename)


async def fetch_details_with_retry(url, max_retries=150, retry_delay=5):
  for attempt in range(max_retries):
    proxies={
        "http": "http://hagllwuk-rotate:itwc7jf4mnqf@p.webshare.io:80/",
        "https": "http://hagllwuk-rotate:itwc7jf4mnqf@p.webshare.io:80/"
      }
    session = AsyncHTMLSession(browser_args=["--no-sandbox", f'--user-agent={ua.random}'])

    response = await session.get(url)
    if response.status_code == 200:
      await response.html.arender(sleep=2,timeout=30)
      html_content = response.html.html
      return html_content

    print(f"Error {response.status_code}, Retrying: {attempt+1}, {url}")
    time.sleep(retry_delay)


async def parse_sellers_details(full_link, name, photo_url, bio,focuses):
    try:

        html_content = await fetch_details_with_retry(full_link)
        soup = BeautifulSoup(html_content, 'lxml')
        try:
          path_tag = soup.find('path', {'d': 'M3.33325 17.5V7.5L9.99992 2.5L16.6666 7.5V17.5H11.6666V11.6667H8.33325V17.5H3.33325Z'})
          parent_svg_tag = path_tag.parent
          grand_parent_div = parent_svg_tag.parent
          location = grand_parent_div.text

        except:
          location = ""

        try:
          json_data_element = soup.find('script', {'id':'__NEXT_DATA__'})
          json_data =json_data_element.text
          data = json.loads(json_data)

          profile = data['props']['pageProps']['profileDetail']

          try:
            website = profile.get('website', '')
          except:
            website = ''

          try:
            twitter = profile.get('twitter', '')
          except:
            twitter = ''
          instagram_handle = profile.get('instagram', '')
          try:
            if not instagram_handle.startswith(('http://', 'https://')):
              instagram_handle = f"https://www.instagram.com/{instagram_handle}"
            profile['instagram'] = instagram_handle
          except:
            instagram_handle = ''



          tiktok = profile.get('tiktok', '')
          youtube = profile.get('youtube', '')

          try:
            language_names = ', '.join(language['name'] for language in profile['languages'])
          except:
            language_names = ''

          try:
            destinations = '; '.join(location['name'] for location in profile['locations'])
          except:
            destinations = ''

          try:
            num_subscribers_element = soup.find('div', class_='mantine-Text-root mantine-s0l6b0')
            num_subscribers = num_subscribers_element.text
          except:
            num_subscribers = ''


        except Exception as e:
          print(f"Oops: {e}")



        data = {
            'Link': full_link,
            'Name': name,
            'Photo': photo_url,
            'Bio': bio,
            'Instagram': instagram_handle,
            'Twitter': twitter,
            'YouTube': youtube,
            'TikTok': tiktok,
            'Blog / Website': website,
            'Location': location,
            'Destinations': destinations,
            'Focuses': focuses,
            'Languages': language_names,
            '# of subscribers': num_subscribers,

        }
        print(name,full_link)

        # return data
        data_list.append(data)

    except Exception as e:
        print(f"Error fetching details for: {e}")