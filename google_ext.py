import datetime
import re
import pandas as pd
import time

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from lxml import etree


def email_ext(text):
    """
    This function extracts the emails from a given text
    with the help of RegEx

    :param text: the HTML response in text format
    :return: Return a list of the extracted emails
    """
    email_list = re.findall(r"[A-Za-z0-9._%+-]{3,}@[A-Za-z0-9.-]+\.[A-Za-z]{2,5}", text, re.M)

    return email_list


#
def site_req(kwrd: str, location: str):
    """
    This function gets the search result for the first
    10 pages of a given keyword/phrase

    :param location: The search location
    :param kwrd: the modules search term/keyword
    :return: returns a list of extracted emails.

    """

    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'}

    page_no = 0

    output = []
    keyword = kwrd.replace(" ", "+")
    sites = ["facebook.com", "twitter.com", "linkedin.com", "instagram.com", "pinterest.com", "tiktok.com","github.com", "discord.com", "hicounselor.com"]
    emails = ["gmail.com",
              "yahoo.com",
              "icloud.com",
              "yahoo.co.uk"]
    # "hotmail.com",
    # "live.com",
    # "aol.com"

    emails = ["%40" + email for email in emails]
    emails = '"' + '"+"'.join(emails) + '"'

    print(emails)
    for site in sites:

        while True:
            with sync_playwright() as p:

                url = f'https://www.google.com/search?q="{keyword}"' \
                      f'+-location:"{location}"+-site:{site}+{emails}&start={page_no}'

                browser = p.chromium.launch()  # Add headless=False to show the browser
                ua = (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/112.0.0.0 Safari/537.36")
                page = browser.new_page(user_agent=ua)
                page.goto(url, wait_until="domcontentloaded")  # wait for content to load
                html = page.content()

                if html:
                    soup = BeautifulSoup(html, "html.parser")
                    dom = etree.HTML(str(soup))
                    print(dom)
                    results = dom.xpath("//div[@class='MjjYud']//div[@data-sncf='1']/div/span")
                    results = [str(s.xpath('.//text()')) for s in results]
                    for result in results:
                        result = result.replace("',", " ")
                        result = result.replace("...", "")
                        result = result.replace("'", "")
                        result = result.replace('"', "")
                        result = result.replace("  ", " ")
                        result = result.replace("[", "")
                        result = result.replace("]", "")
                        result = result.replace("mailto:", "")
                        result = result.split()
                        for i,res in enumerate(result):
                            if res.endswith("@"):
                                res = result[i]+result[i+1]
                                output.append({
                                    "Email": res,
                                    "Keyword": kwrd
                                })

                    print(url)
                    print(output)
                    print(len(output))

                    if page_no == 110:
                        page_no = 0
                        break

                    page_no = page_no + 10

                    time.sleep(5)

                browser.close()

    return output


def google_search(keywords: list, location):
    """
    This function use the site_req() function to perform multiple search with multiple keywords/phrases
    :param keywords:
    :return: Nan
    """
    result = []

    for keyword in keywords:
        req = site_req(keyword, location)
        if req:
            result.extend(req)
    print(len(result))
    return result


# This function saves the resulting list from google_search to a csv file
def run(keywords: list, location):
    """
    This function saves the resulting list from google_search to a csv file

    :param keywords:
    :return:
    """
    lists = google_search(keywords, location)
    data = pd.DataFrame(lists)
    date_time = datetime.datetime.now()
    dt = date_time.strftime("%d_%m_%y_%H_%M")
    data.to_csv(f"google_extract_{dt}.csv", index=False)
