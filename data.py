import csv
import os.path
import requests as r
import datetime as dt

# TODO - Perhaps make it a function that can accept any set of params to create a file for

# get today's date and store it with a string of time format that is identical to what is saved to our csv
todays_date: str = dt.datetime.now().strftime("%a-%d-%b-%y")

# URL to get price data
base_url: str = "https://api.bybit.com"
ohlc_url: str = base_url + "/v5/market/kline"

# TODO - Make a more modular way of creating a file name
FILE_NAME: str = "BTC-1D-PRICE-HISTORY.csv"

# TODO - Add more logging lines
def request_data(data_params) -> None:
    print(f"UPDATING {data_params} RECORDS IN CSV FILE")

    # Call the website
    response = r.get(ohlc_url, params=data_params)

    # Get the list of prices and reverse the order so that they appear in ascending order
    price_list = [row for row in response.json()["result"]["list"]]
    price_list.reverse()

    with open(FILE_NAME, "a", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")

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

            writer.writerow([date, time, open_price, high_price, low_price, close_price, volume])

    # TODO - Add better logging message



def get_last_record() -> str:
    print("RETRIEVING LAST RECORD FROM CSV")
    # open the existing file
    with open(FILE_NAME, "r") as price_file:
        # get a hold of the contents of the file
        all_lines = price_file.readlines()

        # Create a variable for the last record in the csv file, isolating just the date from the file
        last_line: str = all_lines[-1:][0][:13]
    return last_line


def delete_record(num_of_lines: int) -> None:
    print(f"DELETING {num_of_lines} RECORD(S) FROM CSV")
    with open(FILE_NAME, "r") as price_file:
        all_lines = price_file.readlines()
        with open(FILE_NAME, "w") as price_file_2:
            price_file_2.writelines(all_lines[:-num_of_lines])


def update_csv() -> None:
    print("CHECKING IF NEW DATA IS AVAILABLE FOR CSV FILE")

    # Create a file for the data if the file doesn't exist
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w") as new_file:
            # Add the column headers to the file
            print("CREATING CSV")
            new_file.write("date,time,open,high,low,close,volume\n")

        # Param dictionary to download 1000 records (maximum allowed)
        params = {"category": "linear",
                  "symbol": "BTCUSDT",
                  "interval": "D",
                  "limit": 1000
                  }
        request_data(params)

    # Get the last record in the csv file
    last_record: str = get_last_record()

    # Check if the days date matches the last record
    if todays_date != last_record:

        # Param dictionary to download 1 record
        params = {"category": "linear",
                  "symbol": "BTCUSDT",
                  "interval": "D",
                  "limit": 1
                  }

        # download one more record
        request_data(params)
        # get the last record... again
        last_record: str = get_last_record()

        # Check if the dates match again
        if todays_date == last_record:
            delete_record(2)

            # Param dictionary to download 1 record
            params = {"category": "linear",
                      "symbol": "BTCUSDT",
                      "interval": "D",
                      "limit": 2
                      }

            # download one more record
            request_data(params)
        else:
            print(todays_date, type(todays_date), last_record, type(last_record))
            delete_record(2)

            # Param dictionary to download 1 record
            params = {"category": "linear",
                      "symbol": "BTCUSDT",
                      "interval": "D",
                      "limit": 1
                      }

            # download one more record
            request_data(params)

    print("CSV UPDATED")


def main():
    update_csv()


if __name__ == "__main__":
    main()

