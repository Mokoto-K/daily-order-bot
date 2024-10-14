import os
from dotenv import load_dotenv
import ccxt
import bot as nn

load_dotenv()
key: str = os.getenv("API_KEY")
secret: str = os.getenv("API_SECRET")

# Not needed until I rebuild the api from scratch with no prebuilt libraries
# base_url = "https://www.bitmex.com/api/v1"
# create_order_url = base_url+"/order"

mex = ccxt.bitmex({"apiKey": key, "secret": secret})

# CLOSE OPEN POSITION
# Get the size of the open position
open_size = mex.fetch_positions()[0]["contracts"]

# Get the direction of the current position
open_direction = mex.fetch_positions()[0]["side"]

if open_direction == "long":
    close_side = "sell"
elif open_direction == "short":
    close_side = "buy"
else:
    close_side = None

# Uncomment out once finished with testing, this will execute a market order currently, which we don't want yet.
# mex.create_market_order("XBTUSDT", side=close_side, amount=open_size)

# CANCEL ALL ORDERS
mex.cancel_all_orders()

# CALCULATE NEXT POSITION SIZE
account_size = mex.fetch_balance()["USDT"]["total"]
risk_limit = 0.01
risk_amount = account_size * risk_limit /100
current_price = mex.fetch_ticker("XBTUSDT")["bid"]

# Arbitrary stop & profit price (Bad idea long term, but ok for testing atm)
if nn.direction == "long":
    side = "buy"
    stop_price = current_price - (current_price * 0.01)
    stop_difference = (stop_price - current_price) / current_price * -1

    profit_price = current_price + (current_price * 0.01)

    size = risk_amount / stop_difference

    # ENTER NEW POSITION
    # mex.create_market_order("XBTUSDT", "limit", side, price=current_price, amount=size)

    # ADD STOP AND TAKE PROFIT
    # mex.create_stop_market_order("XBTUSDT", "sell", size, stop_price)
    # mex.create_limit_order("XBTUSDT", "sell", size, profit_price)

else:
    side = "sell"
    stop_price = current_price + (current_price * 0.01)
    stop_difference = (stop_price - current_price) / current_price

    profit_price = current_price - (current_price * 0.01)

    size = risk_amount / stop_difference

    # ENTER NEW POSITION
    # mex.create_market_order("XBTUSDT", "limit", side, price=current_price, amount=size)

    # ADD STOP AND TAKE PROFIT
    # mex.create_stop_market_order("XBTUSDT", "buy", size, stop_price)
    # mex.create_limit_order("XBTUSDT", "buy", size, profit_price)
