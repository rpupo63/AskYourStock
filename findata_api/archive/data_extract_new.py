import math
import numpy as np
import yfinance as yf
import time

NUM_VALUES_TO_READ = 200  # Assuming this variable might still be relevant for your use case

# Function to fetch and prepare data from Yahoo Finance
def fetch_data_from_yahoo(ticker, start_date='2018-01-01', end_date='2018-12-31'):
    stock = yf.Ticker(ticker)
    stock_data = stock.option_chain(date = '2024-02-23')
    data = stock_data.calls
    return data

# Adapted function to extract data for a chosen stock
def extract_data_yahoo(ticker):
    ticker = str(ticker)  # Convert ticker to string to ensure compatibility
    print('Fetching data for', ticker)
    data = fetch_data_from_yahoo(ticker)
    # Rest of the function...
    print("Here's the data:")
    print(data)

    
    # Extracting relevant features
    prices = data.lastPrice.values
    bid = data.bid
    ask = data.ask  
    pe = np.nan
    high = np.nan
    low = np.nan
    volume = np.nan
    turnover = np.nan
    
    all_prices_list = [prices, bid, ask, pe, high, low, volume, turnover]
    
    # Handling missing data as in your original function
    max_len = max([len(feature) for feature in all_prices_list])
    
    for i in range(len(all_prices_list)):
        feature = all_prices_list[i]
        len_diff = max_len - len(feature)
        feature_list = feature.tolist()
        new_list = []
        prev_x = 0.0
        for x in feature_list:
            if math.isnan(x):
                x = prev_x
            new_list.append(x)
            prev_x = x
        feature_list = new_list
        if len(feature_list) > 0:
            first_value = feature_list[0]
            for _ in range(len_diff):
                feature_list.insert(0, first_value)
        else:
            feature_list = [0.0] * max_len
        all_prices_list[i] = feature_list
    
    array = np.array(all_prices_list)
    array = np.expand_dims(array, axis=0)  # Adding the stock dimension, resulting in (1, f, t)
    
    print('Data shape:', array.shape)
    return array

# Example usage with a single stock
if __name__ == '__main__':
    ticker = str('AAPL')  # Feed data in here
    print(ticker)
    main_start_time = time.time()
    extract_data_yahoo(ticker)
    main_end_time = time.time()
    print('Time spent: {:.2f} seconds'.format(main_end_time - main_start_time))
