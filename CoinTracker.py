import requests
from bs4 import BeautifulSoup
import os
from twilio.rest import Client
from slack_sdk import WebClient

#scrape Greed&Fear Index
gf_url = 'https://alternative.me/crypto/fear-and-greed-index/'
gf_response = requests.get(gf_url)
gf_soup = BeautifulSoup(gf_response.content, 'html.parser')

gf_box = gf_soup.find('div', class_ = 'fng-value')
gf_index_today = gf_box.find('div', class_ = 'fng-circle').get_text()
gf_status_today = gf_box.find('div', class_ = 'status').get_text()
gf_time_today = gf_box.find('div', class_ = 'gray').get_text()

#scrape AltCoin Season Index
alt_url = 'https://www.blockchaincenter.net/en/altcoin-season-index/'
alt_response = requests.get(alt_url)
alt_soup = BeautifulSoup(alt_response.content, 'html.parser')

alt_box = alt_soup.find('button', class_ = 'nav-link timeselect active')
alt_index_today = alt_box.find('b').get_text()

gf_message = "The greed and fear index today is " + gf_index_today + ", which is " + gf_status_today
alt_message = "\n < 25 being bitcoin and > 75 being altcoin." + " Today's index is " + alt_index_today

message = gf_message + "\n" + alt_message

client = WebClient(token=os.environ["SLACK_TOKEN"])

client.chat_postMessage(
    channel="greedandfear",
    text = message,
    username="Greed&Fear"
)