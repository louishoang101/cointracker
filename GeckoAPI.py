
import requests
import os
from twilio.rest import Client
from slack_sdk import WebClient

url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&price_change_percentage=1h"

headers = {
'accept': 'application/json',
'x-cg-demo-api-key': os.environ['GECKO_KEY']
}
response = requests.get(url, headers=headers)
coin_list = response.json()

#FORMULA
formula = "SYMBOL:CURR:1H:24H"

#GETTING BTC
btc = f"{str(coin_list[0]['symbol']).upper()}:{coin_list[0]['current_price']}:{coin_list[0]['price_change_percentage_24h']}:{coin_list[0]['price_change_percentage_1h_in_currency']}"

filtered_coins = [coin for coin in coin_list if 200000000 < coin["market_cap"] < 2000000000]

sorted_coins = sorted(filtered_coins, key=lambda x:x["price_change_percentage_1h_in_currency"], reverse=True)

top_coins = sorted_coins[:20]
list_midcap = []
for coin in top_coins:
    list_midcap.append(f'{coin["symbol"].upper()}:{round(coin["current_price"],4)}:{round(coin["price_change_percentage_1h_in_currency"],2)}:{round(coin["price_change_percentage_24h"],2)}')

filtered_coins_sc = [coin for coin in coin_list if 20000000 < coin["market_cap"] <= 200000000]

sorted_coins_sc = sorted(filtered_coins_sc, key = lambda x:x["price_change_percentage_1h_in_currency"], reverse=True)
top_coins_sc = sorted_coins_sc[:20]
list_smallcap = []
for coin in top_coins_sc:
    list_smallcap.append(f'{coin["symbol"].upper()}:{round(coin["current_price"],4)}:{round(coin["price_change_percentage_1h_in_currency"],2)}:{round(coin["price_change_percentage_24h"],2)}')

message = formula + "\n\n" + btc + "\n\n" + "Here is the list of top 20 coins (MID-CAP) with most 1h change: \n" + str(list_midcap)+ '\n' + "\nHere is the list of top 20 coins (SMALL-CAP) with most 1h change: \n" + str(list_smallcap)

client = WebClient(token=os.environ["SLACK_TOKEN"])

client.chat_postMessage(
    channel="crypto-updates",
    text = message,
    username="CryptoUpdates"
)
