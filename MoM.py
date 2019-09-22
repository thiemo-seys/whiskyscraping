import requests
from bs4 import BeautifulSoup
import datetime
from managers import email
import logging

logging.basicConfig(level=logging.DEBUG, filename="app.log", filemode="w")

url = "https://www.masterofmalt.com/new-arrivals/whisky-new-arrivals/"
currentDay = datetime.datetime.now().day
succes_message = "New bottles have been released on Mom!"

response = requests.get(url)
bs = BeautifulSoup(response.text, "html.parser")
test = bs.find('div', {"class": "col-xs-4 col-sm-2 h-gutter"})
day = int(test.find('span').text)
if currentDay == day:
    print("new whisky has been released")
    logging.info("new whisky has been released")
    email.send_email(message=succes_message)

