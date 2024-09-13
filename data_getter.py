import yfinance as yf
from datetime import datetime
import time


def data_getter(file="stocks.txt", interval="1d"):
    stock_list = []
    with open(file) as file:
        while line := file.readline():
            stripped_line = line.rstrip()
            if stripped_line:
                stock_list.append(stripped_line)

    # GET TODAY'S DATE AND CONVERT IT TO A STRING WITH YYYY-MM-DD FORMAT (YFINANCE EXPECTS THAT FORMAT)
    end_date = datetime.now().strftime('%Y-%m-%d')

    start_time_total = time.time()

    for stock in stock_list:
        start_time = time.time()
        curr_stock = yf.Ticker(stock)

        stock_hist = curr_stock.history(period="max", end=end_date, interval=interval)

        print("Gathered stock history for: " + stock)

        file_save_name = "stock_data/" + stock + ".csv"

        stock_hist.to_csv(file_save_name)
        print("Successfully saved stock data for: " + stock + " as " + file_save_name)

        end_time = time.time()
        time_diff = round(end_time - start_time, 3)

        print("Gathered data for: " + stock + " in: " + str(time_diff) + "s\n")

    end_time_total = time.time()
    time_diff = round(end_time_total - start_time_total, 3)

    print("Finished gathering all data in: " + str(time_diff) + "s")

    return sorted(stock_list)


if __name__ == "__main__":
    stocks = data_getter()
