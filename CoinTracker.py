import requests
from bs4 import BeautifulSoup
import os
from twilio.rest import Client

#Set up twilio account via API
account_sid = os.environ["TWILIO_ACC_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
print(account_sid)
print(auth_token)
client = Client(account_sid, auth_token)

from_whatsapp_number = 'whatsapp:+14155238886'
to_whatsapp_number = 'whatsapp:+61431515817'

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

client.messages.create(body = gf_message + alt_message,
                   from_ = from_whatsapp_number,
                   to = to_whatsapp_number)