import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import os

Legacy_list = ['technology.csv',
               'healthcare.csv',
               'financials.csv',
               'consumer_discretionary.csv',
               'consumer_staples(2.0).csv',
               'Industrials(2.0).csv',
               'energy.csv',
               '20260129_Utilities.csv',
               'materials.csv',
               'telecommunications.csv',
               'real-estate.csv']
New_list = ['Completed_trades/Technology_trades.csv',
            'Completed_trades/Healthcare_trades.csv',
            'Completed_trades/Financials_trades.csv',
            'Completed_trades/Consumer_Discretionary_trades.csv',
            'Completed_trades/Consumer_Staples_trades.csv',
            'Completed_trades/Industrials_trades.csv',
            'Completed_trades/Energy_trades.csv',
            'Completed_trades/Utilities_trades.csv',
            'Completed_trades/Materials_trades.csv',
            'Completed_trades/Telecommunications_trades.csv',
            'Completed_trades/Real_Estate_trades.csv']

for i in range(len(Legacy_list)):
    Legacy_file = Legacy_list[i]
    New_file = New_list[i]

    df_legacy = pd.read_csv(Legacy_file)
    df_newfile = pd.read_csv(New_file)

    for index, row in df_legacy.iterrows():
        date_string = row['Date(YYYY-MM-DD)']
        datetime_object = datetime.strptime(date_string, "%Y-%m-%d").date()
        if datetime_object.weekday() == 4:
            next_date = datetime_object + timedelta(days=3)
            check_date = 'SAT'
        elif datetime_object.weekday() == 5:
            next_date = datetime_object + timedelta(days=2)
            check_date = 'SUN'
        else:
            next_date = datetime_object + timedelta(days=1)
            check_date = 'PASS'

        print(datetime_object,' ',type(datetime_object),' ',next_date,' ',check_date)
        After_date = next_date + timedelta(days=1)
        
        try:
            stock_data = yf.download(row['Ticker'], start=next_date, end=After_date)
            while stock_data.empty:
                next_date = After_date
                After_date = After_date + timedelta(days = 1)
                stock_data = yf.download(row['Ticker'], start=next_date, end=After_date)
            open_price = stock_data['Open'].iloc[0].values[0]
        except Exception as e:
            print(f"Error fetching {row['Ticker']}: {e}. Skipping.")
            continue

        Executed_date = next_date
        Executed_Action = row['Action(buy/sell)']
        Executed_Amount = row['Number of units']
        Ticker = row['Ticker']
        Executed_price = open_price

        new_row_limit_order = {
            'Date(YYYY-MM-DD)': Executed_date,
            'Action(buy/sell)': Executed_Action,
            'Number of units': Executed_Amount,
            'Ticker': Ticker,
            'Price': Executed_price
        }
        df_newfile = pd.concat([df_newfile, pd.DataFrame([new_row_limit_order])], ignore_index=True)

    df_newfile.to_csv(New_file, index = False)