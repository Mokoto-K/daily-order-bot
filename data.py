import csv
import os.path
import requests as r
import datetime as dt

# TODO - Perhaps make it a function that can accept any set of params to create a file for

# URL to get price data
base_url = "https://api.bybit.com"
ohlc_url = base_url+"/v5/market/kline"

# Param dictionary for whatever you are looking for
params = {"category": "linear",
          "symbol": "BTCUSDT",
          "interval": "D",
          "limit": 100
          }

# Call the website
response = r.get(ohlc_url, params=params)

# TODO - Make a more modular way of creating a file name
file_name = "BTC-1D-PRICE-HISTORY.csv"

# Create a file for the data if the file doesn't exist
if not os.path.exists(file_name):
    with open(file_name, "w") as price_file:
        price_file.write("date,time,open,high,low,close,volume\n")

# Get the list of prices and reverse the order so that they appear in ascending order
price_list = [row for row in response.json()["result"]["list"]]
price_list.reverse()

with open(file_name, "a", newline="") as price_file:
    writer = csv.writer(price_file, delimiter=",")

    for line in range(len(price_list)):
        # Isolate the UTC timestamp, divide by 1000 due to "fromdatestamp" doesn't use the full utc stamp
        timestamp: float = int(price_list[line][0]) / 1000

        # Format the date and time for the line entry
        date: str = dt.datetime.fromtimestamp(timestamp).strftime("%a-%d-%b-%y")
        time: str = dt.datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")

        open_price = round(float(price_list[line][1]))
        high_price = round(float(price_list[line][2]))
        low_price = round(float(price_list[line][3]))
        close_price = round(float(price_list[line][4]))
        volume = round(float(price_list[line][5])) * open_price - close_price

        writer.writerow([date,time,open_price,high_price,low_price,close_price,volume])

