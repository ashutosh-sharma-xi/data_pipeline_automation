import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
from utils import *
import json

logger = setup_logger()

banks_ticker_dict = {"HDFC":"HDB", "SBI":"SBIN.NS" , "ICICI":"IBN"}

def lambda_handler():
  event = {"num_days":10}
  days = event.get("num_days")
  for bank , ticker_symbol in banks_ticker_dict.items():
    try:
        data = get_stock_data(bank , ticker_symbol, days)
        # Assuming 'data' is your DataFrame containing the financial data
        data['Weighted Average Price'] = calculate_weighted_average_price(data)
        data['Daily Price Range'] = calculate_daily_price_range(data)
        data['Price Change Percentage'] = calculate_price_change_percentage(data)
        data['5-Day Moving Average'] = calculate_moving_average(data, window=3)
        data['Volume Weighted Average Price'] = calculate_volume_weighted_average_price(data)
        print(f"\nData of {bank}, {data.columns }")
        # Convert DataFrame to list of tuples
        data.reset_index(inplace=True)
        data_tuple = [tuple(x) for x in data.to_numpy()]
        print("\n\n\nthis is the data:",data)

        print("\n\n\nthis is the tuple:",data_tuple)

        # Pass data_tuple to store_in_rds
        store_in_rds(table_name=bank, data_tuple=data_tuple)
    except Exception as e:
        logger.error("Error occured while fetching data...",e)

def calculate_weighted_average_price(data):
    wap = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    return wap

def calculate_daily_price_range(data):
    daily_range = data['High'] - data['Low']
    return daily_range

def calculate_price_change_percentage(data):
    price_change_percentage = ((data['Close'] - data['Close'].shift(1)) / data['Close'].shift(1)) * 100
    return price_change_percentage

def calculate_moving_average(data, window=3):
    moving_average = data['Close'].rolling(window=window).mean()
    return moving_average

def calculate_volume_weighted_average_price(data):
    vwap = (data['Close'] * data['Volume']).cumsum() / data['Volume'].cumsum()
    return vwap

def convert_to_df(data):
  df = pd.DataFrame(data)
  return df


def get_stock_data(bank, symbol, days):
    try:
        # Define the start and end dates for the historical data
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        # Fetch historical data from Yahoo Finance
        data = yf.download(symbol, start=start_date, end=end_date)
        df = convert_to_df(data)
        return df
    except Exception as e:
        logger.error(f"Failed to fetch data for {bank} ({symbol}): {e}")
        return None

def store_in_rds(table_name, data_tuple):
    try:
        secrets = get_db_secret()
        conn, cursor = db_connection(secrets)
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
        Date DATE NOT NULL PRIMARY KEY,  
        Open NUMERIC(10,2) NOT NULL,  
        High NUMERIC(10,2) NOT NULL, 
        Low NUMERIC(10,2) NOT NULL,   
        Close NUMERIC(10,2) NOT NULL, 
        Adj_Close NUMERIC(10,2) NOT NULL, 
        Volume BIGINT NOT NULL,  
        Weighted_Average_Price NUMERIC(10,4) NOT NULL,  
        Daily_Price_Range VARCHAR(255) NOT NULL,  
        Price_Change_Percentage NUMERIC(5,2) NOT NULL, 
        "5-Day_Moving_Average" NUMERIC(10,2) NOT NULL,  
        Volume_Weighted_Average_Price NUMERIC(10,4) NOT NULL
        );
        """
        cursor.execute(create_table_query)
        columns = [
                    "Date",
                    "Open",
                    "High",
                    "Low",
                    "Close",
                    "Adj_Close",
                    "Volume",
                    "Weighted_Average_Price",
                    "Daily_Price_Range",
                    "Price_Change_Percentage",
                    "5-Day_Moving_Average",
                    "Volume_Weighted_Average_Price"
                ]


        query = "INSERT INTO your_table ({}) VALUES {}".format(
            ', '.join(columns),
            ', '.join(['%s'] * len(data_tuple))
        )
        
        # Execute the query
        cursor.executemany(query, data_tuple)
        # Commit the transaction
        conn.commit()
        # Close cursor and connection
        cursor.close()
        conn.close()

    except Exception as e:
        logger.error("Failed to store to db", e)
        raise e
lambda_handler()