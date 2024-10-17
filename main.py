# import data
import os
from dotenv import load_dotenv
import ccxt
import algorithm as algo
import data

RISK = 0.01

load_dotenv()
key: str = os.getenv("API_KEY")
secret: str = os.getenv("API_SECRET")

# Not needed until I rebuild the api from scratch with no prebuilt libraries
# base_url = "https://www.bitmex.com/api/v1"
# create_order_url = base_url+"/order"

# TODO - Handle all null cases when querying bitmex for positions, accounts, and orders.

mex = ccxt.bitmex({"apiKey": key, "secret": secret})


# TODO - Add logging information about the position
def close_position() -> None:
    """Queries bitmex for your current open position and market closes it immediately"""
    print("CLOSING LAST POSITION")

    try:
        # Get the size of the open position
        position = mex.fetch_positions()[0]
        # TODO - Find out what error is thrown if no order is open
    except Exception:
        print("There was no position to close, moving on to cancelling open orders")
        return

    # Get the direction of the current position
    open_direction: str = position["side"]
    open_size: float = position["contracts"]

    if open_direction == "long":
        close_side = "sell"
    else:
        close_side = "buy"

    # Uncomment out once finished with testing, this will execute a market order currently, which we don't want yet.
    # mex.create_market_order("XBTUSDT", side=close_side, amount=open_size)
    print(f"close {open_direction} of {open_size} contracts...... add profit/loss message")


def cancel_all() -> None:
    """Cancels all orders that you have open on bitmex"""
    print("CANCELLING ORDERS")
    # CANCEL ALL ORDERS
    mex.cancel_all_orders()
    print("All order from the last position have been cancelled")


def execute_trade(risk: float) -> None:
    """"""
    print("RUNNING ALGO TO DETERMINE NEXT DIRECTION AND POSITION SIZE")
    # CALCULATE NEXT POSITION SIZE
    account_size = mex.fetch_balance()["USDT"]["total"]
    risk_limit = risk
    risk_amount = account_size * risk_limit / 100
    current_price = mex.fetch_ticker("XBTUSDT")["bid"]

    direction: str = algo.run_bot()
    # Arbitrary stop & profit price (Bad idea long term, but ok for testing atm)
    if direction == "buy":
        side = "buy"
        stop_price = current_price - (current_price * 0.01)
        stop_difference = (stop_price - current_price) / current_price * -1

        profit_price = current_price + (current_price * 0.01)

        size = risk_amount / stop_difference

        # ENTER NEW POSITION
        # mex.create_market_order("XBTUSDT", side, price=current_price, amount=size)
        print(f"{side}, {size} contracts of XBTUSDT, at: {current_price}, stop: {stop_price}, take profit: {profit_price}")
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
        # mex.create_market_order("XBTUSDT", side, price=current_price, amount=size)
        print(f"{side}, {size} contracts of XBTUSDT, at: {current_price}, stop: {stop_price}, take profit: {profit_price}")
        # ADD STOP AND TAKE PROFIT
        # mex.create_stop_market_order("XBTUSDT", "buy", size, stop_price)
        # mex.create_limit_order("XBTUSDT", "buy", size, profit_price)


def main() -> None:
    # Close previous days trade
    close_position()

    # Cancel an open orders that remain
    cancel_all()

    # Update csv for current data from exchange
    data.update_csv()

    # Get direction of trade from nn
    # Get entry, exit and size for trade
    # Execute trade
    execute_trade(RISK)

if __name__ == "__main__":
    main()

