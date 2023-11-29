import datetime
import re
import pandas as pd
import requests
import time


def email_ext(text):
    """
    This function extracts the emails from a given text
    with the help of RegEx

    :param text: the HTML response in text format
    :return: Return a list of the extracted emails
    """
    email_list = re.findall(r"[A-Za-z0-9_.-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,5}", text, re.M)

    return email_list


#
def site_req(keyword: str):
    """
    This function gets the search result for the first
    10 pages of a given keyword/phrase

    :param keyword: the modules search term/keyword
    :return: returns a list of extracted.

    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'}

    page = 0

    result = []
    location = "United States"
    keyword = keyword.replace(" ", "+")
    sites = ["facebook.com", "twitter.com", "linkedin.com", "instagram.com", "pinterest.com", "tiktok.com"]
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
            url = f'https://www.google.com/search?q="{keyword}"+-location:"{location}"+-site:{site}+{emails}&start={page}'
            print(url)
            print(keyword)
            print(site)

            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                break

            text = response.text
            result.extend(email_ext(text))
            print(result)

            if page == 110:
                page = 0
                break

            page = page + 10

            time.sleep(5)

    return result


def google_search(keywords: list):
    """
    This function use the site_req() function to perform multiple search with multiple keywords/phrases
    :param keywords:
    :return: Nan
    """
    result = []

    for keyword in keywords:
        req = site_req(keyword)
        if req:
            result.extend(req)
    print(len(result))
    return result


# This function saves the resulting list from google_search to a csv file
def run(keywords: list):
    """
    This function saves the resulting list from google_search to a csv file

    :param keywords:
    :return:
    """
    lists = google_search(keywords)
    data = pd.DataFrame(lists)
    date_time = datetime.datetime.now()
    dt = date_time.strftime("%d_%m_%y_%H_%M")
    data.to_csv(f"google_extract_{dt}.csv", index=False)
