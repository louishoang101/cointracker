
import requests
import json 
import pendulum
import time
from datetime import datetime
import os
from twilio.rest import Client

#Set up twilio account via API
account_sid = os.environ['TWILIO_ACC_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

client = Client(account_sid, auth_token)

from_whatsapp_number = 'whatsapp:+14155238886'
to_whatsapp_number = 'whatsapp:+61431515817'

headers = f"{
'accept': 'application/json',
'x-cg-demo-api-key': {os.environ['GECKO_KEY']}
}"
url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&price_change_percentage=1h"

response = requests.get(url, headers=headers)
coin_list = response.json()

#FORMULA
formula = "SYMBOL:CURR:24H:1H"

#GETTING BTC
btc = f"{str(coin_list[0]['symbol']).upper()}:{coin_list[0]['current_price']}:{coin_list[0]['price_change_percentage_24h']}:{coin_list[0]['price_change_percentage_1h_in_currency']}"

filtered_coins = [coin for coin in coin_list if 200000000 < coin["market_cap"] < 2000000000]

sorted_coins = sorted(filtered_coins, key=lambda x:x["price_change_percentage_24h"], reverse=True)

top_coins = sorted_coins[:20]
list_midcap = []
for coin in top_coins:
    list_midcap.append(f'{coin["symbol"].upper()}:{round(coin["price_change_percentage_24h"],2)}:{round(coin["price_change_percentage_1h_in_currency"],2)}')

filtered_coins_sc = [coin for coin in coin_list if 20000000 < coin["market_cap"] <= 200000000]

sorted_coins_sc = sorted(filtered_coins_sc, key = lambda x:x["price_change_percentage_24h"], reverse=True)
top_coins_sc = sorted_coins_sc[:20]
list_smallcap = []
for coin in top_coins_sc:
    list_smallcap.append(f'{coin["symbol"].upper()}:{round(coin["price_change_percentage_24h"],2)}:{round(coin["price_change_percentage_1h_in_currency"],2)}')

#return "Here are the list of top 20 coins (MID-CAP) with most 24h change: \n" + str(list_midcap)+ '\n' + "\nHere are the list of top 20 coins (SMALL-CAP) with most 24h change: \n" + str(list_smallcap)
client.messages.create(body = formula + "\n\n" + btc + "\n\n" + "Here is the list of top 20 coins (MID-CAP) with most 24h change: \n" + str(list_midcap)+ '\n' + "\nHere is the list of top 20 coins (SMALL-CAP) with most 24h change: \n" + str(list_smallcap),
                    from_ = from_whatsapp_number,
                    to = to_whatsapp_number)
