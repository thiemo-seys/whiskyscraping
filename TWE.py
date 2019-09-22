import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import datetime
from managers import email
import logging

#variables
base = "https://www.thewhiskyexchange.com/new-products/"
url_standard = base + "standard-whisky#nav"
url_rare = base + "old-and-rare-whisky#nav"
currentDay = datetime.datetime.now().day

#global lsits
urls = []
responses = []
parsed_htmls = []
previous_release_days = []
#add data to lists
urls.append(url_standard)
urls.append(url_rare)

for url in urls:
    responses.append(requests.get(url))

for response in responses:
    if response.status_code == 200:
        parsed_htmls.append(BeautifulSoup(response.text, "html.parser"))


for text in parsed_htmls:
    list_days_strings = ([item.get_text(strip=True) for item in text.select("span.np-posthead__date-day")])
    #parse days to int (there should be a cleaner way to do this right?
    days = [int(i) for i in list_days_strings]
    previous_release_days.append(days)


for releases in previous_release_days:
    if releases[0] == currentDay:
        print("new bottles have come out")
        email.send_email()
    else: print("no new bottles have been release")
