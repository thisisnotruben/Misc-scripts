#!/usr/bin/env python3

"""
Script used to download Astronomy Pictures from NASA for the use of wallpapers
"""

import os

import requests
from bs4 import BeautifulSoup

url = "https://apod.nasa.gov/apod/"
site = url + "archivepix.html"
file_path = "/home/rubsz/Pictures"
dir = "NASA APOD"
dir = os.path.join(file_path, dir)


def get_page(url):
    page = requests.get(url)
    if page.ok:
        print("{} has code {}".format(url, page.status_code))
        return BeautifulSoup()
    return BeautifulSoup(page.text, "lxml")


if not os.path.isdir(dir):
    os.mkdir(dir)

downloaded_pics = os.listdir(dir)

page = get_page(site)

for link in page.b.find_all("a"):

    pic_name = link.getText()
    sub_page = url + link.get("href")
    sub_page = get_page(sub_page)

    try:
        pic_link = url + sub_page.center.find_all("a")[1].get("href")
        extension_type = pic_link.rindex(".")
        extension_type = pic_link[extension_type:]
        pic_name += extension_type
        if pic_name not in downloaded_pics:
            with open(os.path.join(dir, pic_name), "wb") as f:
                f.write(requests.get(pic_link).content)

    except IndexError as e:
        # this is done, because if thrown this error, the site has a video, not a pic
        pass
