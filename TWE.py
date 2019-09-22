import requests
from bs4 import BeautifulSoup
import datetime
from managers import email
import logging

logging.basicConfig(level=logging.DEBUG, filename="app.log", filemode="w")

# variables
base = "https://www.thewhiskyexchange.com/new-products/"
succes_message = "New bottles have been released on Mom!"
currentDay = datetime.datetime.now().day

# global lsits
urls = [base + "standard-whisky#nav", base + "old-and-rare-whisky#nav"]
responses = []
parsed_htmls = []
previous_release_days = []

logging.info("starting http requests")
for url in urls:
    logging.debug("get requesting:" + url)
    responses.append(requests.get(url))

logging.info("starting html parsing")
for response in responses:
    if response.status_code == 200:
        parsed_htmls.append(BeautifulSoup(response.text, "html.parser"))
        logging.debug("parsed html")
    else:
        logging.warning("failed to succesfuly request info, error code: " + response.status_code)

for text in parsed_htmls:
    try:
        list_days_strings = ([item.get_text(strip=True) for item in text.select("span.np-posthead__date-day")])
        # parse days to int (there should be a cleaner way to do this right?
        days = [int(i) for i in list_days_strings]
        # appends all release days to a list, (technically we only need the latest release date) This is WIP, might make the code cleaner but less flexible if we only save the latest release date.
        previous_release_days.append(days)
    except ValueError as e:
        logging.critical("fault in parsing days: " + e)

for releases in previous_release_days:
    # checks if last release day equals the current day.
    if releases[0] == currentDay:
        print("new bottles have come out")
        logging.info("new bottles have been released, sending email")
        email.send_email(message=succes_message)
    else:
        print("no new bottles have been release")
        logging.info("no new bottles have been released today!")
