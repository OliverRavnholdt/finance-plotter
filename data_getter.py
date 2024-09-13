import yfinance as yf           # Used to pull stock data from Yahoo Finance
from datetime import datetime   # Used to specify date for stock pulling
import time                     # Used to track time usage of functions


# Function to pull data from Yahoo Finance
def data_getter(file="stocks.txt", interval="1d", directory="stock_data"):
    stock_list = []     # Create empty list to store stock names

    # Open, read, save and close file with stock names
    with open(file) as file:
        while line := file.readline():
            stripped_line = line.rstrip()
            if stripped_line:
                stock_list.append(stripped_line)

    # GET TODAY'S DATE AND CONVERT IT TO A STRING WITH YYYY-MM-DD FORMAT (YFINANCE EXPECTS THAT FORMAT)
    end_date = datetime.now().strftime('%Y-%m-%d')

    start_time_total = time.time()      # Start time used for tracking total time

    # Pull data from Yahoo Finance for each stock
    for stock in stock_list:
        start_time = time.time()    # Start time used for tracking each pull

        # Get stock data as DataFrame
        curr_stock = yf.Ticker(stock)
        stock_hist = curr_stock.history(period="max", end=end_date, interval=interval)
        print("Gathered stock history for: " + stock)

        # Save data as CSV file in wanted directory
        file_save_name = directory + "/" + stock + ".csv"
        stock_hist.to_csv(file_save_name)
        print("Successfully saved stock data for: " + stock + " as " + file_save_name)

        # Calculate time usage and display to console
        end_time = time.time()
        time_diff = round(end_time - start_time, 3)
        print("Gathered data for: " + stock + " in: " + str(time_diff) + "s\n")

    # Get total time used to get all data and display to console
    end_time_total = time.time()
    time_diff = round(end_time_total - start_time_total, 3)
    print("Finished gathering all data in: " + str(time_diff) + "s")

    return sorted(stock_list)


if __name__ == "__main__":
    stocks = data_getter()
