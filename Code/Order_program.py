import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import os

#initialize files
Trades_list = ['Completed_trades/Test_trade.csv',
               'Completed_trades/Technology_trades.csv',
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
Order_list = ['Order_files/Test_order.csv',
              'Order_files/Technology_order.csv',
              'Order_files/Healthcare_order.csv',
              'Order_files/Financials_order.csv',
              'Order_files/Consumer_Discretionary_order.csv',
              'Order_files/Consumer_Staples_order.csv',
              'Order_files/Industrials_order.csv',
              'Order_files/Energy_order.csv',
              'Order_files/Utilities_order.csv',
              'Order_files/Materials_order.csv',
              'Order_files/Telecommunications_order.csv',
              'Order_files/Real_Estate_order.csv']

CHANGELOG = 'Code/Automatically_completed_trades.csv'

#initialize variables
action_taken = 'Action(mb/ms/lb/ls/sl/sb)'
#trigger_price = 'TriggerPrice'

for i in range(len(Trades_list)):
    ORDER_FILE = Order_list[i]
    TRADE_FILE = Trades_list[i]

    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    #ignore sundays and saturdays
    #if yesterday.weekday() == 5 or yesterday.weekday() == 6:
    #    continue
    
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    today_str = today.strftime('%Y-%m-%d')

#dates for showcase
    today_str = "2026-01-16"
    yesterday_str = "2026-01-15"

    if os.path.exists(ORDER_FILE):
        df_orders = pd.read_csv(ORDER_FILE)
    else:
        print("No stop/limit file found.")
        continue

    if os.path.exists(TRADE_FILE):
        df_buy_sell = pd.read_csv(TRADE_FILE)
    else:
        df_buy_sell = pd.DataFrame(columns=['Date(YYYY-MM-DD)', 'Action(buy/sell)', 'Number of units', 'Ticker','Price'])

    if os.path.exists(CHANGELOG):
        changelog = pd.read_csv(CHANGELOG)
    else:
        changelog = pd.DataFrame(columns=['Date','Action'])
    print(changelog)

    #strip whitespace & change to str
    df_orders.columns = df_orders.columns.str.strip()

    #Actual Order handling
    for index, row in df_orders.iterrows():
        #Check if the order is already complete
        if df_orders.loc[index,'Status'] == 'Complete':
            continue

        if df_orders.loc[index,'Status'] != 'Active':
            df_orders.loc[index,'Status'] = 'Active'

        #Check if order date is valid
        if df_orders.loc[index, 'Date(YYYY-MM-DD)'] >= yesterday_str:
            continue
        
        # Fetch yesterday's high and low
        try:
            stock_data = yf.download(row['Ticker'], start=yesterday_str, end=today_str)
            if stock_data.empty:
                print(f"No data for {row['Ticker']}. Skipping.")
                continue
            high_price = stock_data['High'].iloc[0].values[0]
            low_price = stock_data['Low'].iloc[0].values[0]
            open_price = stock_data['Open'].iloc[0].values[0]
        except Exception as e:
            print(f"Error fetching {row['Ticker']}: {e}. Skipping.")
            continue
        
    # Determine if order is triggered
        triggered = False

        #MARKET ORDERS
        if row[action_taken].lower().strip() == 'marketbuy' or row[action_taken].lower().strip() == 'marketsell':
            triggered = True

        #LIMIT ORDERS
        elif row[action_taken].lower().strip() == 'limitbuy' and low_price <= row['TriggerPrice']:
            triggered = True
        elif row[action_taken].lower().strip() == 'limitsell' and high_price >= row['TriggerPrice']:
            triggered = True
        
        #STOP LOSS AND STOP BUY
        elif row[action_taken].lower().strip() == 'stoploss' and low_price <= row['TriggerPrice']:
            triggered = True
        elif row[action_taken].lower().strip() == 'stopbuy' and high_price >= row['TriggerPrice']:
            triggered = True

        if triggered:
        #Complete the order
            df_orders.loc[index,'Status'] = 'Complete'

        #Figure out correct price and action
            if row[action_taken].lower().strip() == 'marketbuy':
                Executed_action = 'buy'
                Executed_price = open_price
            elif row[action_taken].lower().strip() == 'marketsell':
                Executed_action = 'sell'
                Executed_price = open_price

            elif row[action_taken].lower().strip() == 'limitbuy':
                Executed_action = 'buy'
                if row['TriggerPrice'] >= open_price:
                    Executed_price = open_price
                elif row['TriggerPrice'] <= open_price and row['TriggerPrice'] >= low_price:
                    Executed_price = float(row['TriggerPrice'])
            
            elif row[action_taken].lower().strip() == 'limitsell':
                Executed_action = 'sell'
                if row['TriggerPrice'] <= open_price:
                    Executed_price = open_price
                elif row['TriggerPrice'] >= open_price and row['TriggerPrice'] <= high_price:
                    Executed_price = float(row['TriggerPrice'])
                
            elif row[action_taken].lower().strip() == 'stoploss':
                Executed_action = 'sell'
                if row['TriggerPrice'] >= open_price:
                    Executed_price = open_price
                elif row['TriggerPrice'] <= open_price and row['TriggerPrice'] >= low_price:
                    Executed_price = float(row['TriggerPrice'])
            
            elif row[action_taken].lower().strip() == 'stopbuy':
                Executed_action = 'buy'
                if row['TriggerPrice'] <= open_price:
                    Executed_price = open_price
                elif row['TriggerPrice'] >= open_price and row['TriggerPrice'] <= high_price:
                    Executed_price = float(row['TriggerPrice'])

        # Append to buy/sell
            new_row_limit_order = {
                'Date(YYYY-MM-DD)': yesterday_str,
                'Action(buy/sell)': Executed_action,
                'Number of units': int(row['Number of units']),
                'Ticker': row['Ticker'],
                'Price': Executed_price
            }
            df_buy_sell = pd.concat([df_buy_sell, pd.DataFrame([new_row_limit_order])], ignore_index=True)
            print(f"Triggered and added: {new_row_limit_order}")

            new_row_changelog = {
                'Date':yesterday_str,
                'Action': f'Order date: {row["Date(YYYY-MM-DD)"]} | Order team: {ORDER_FILE} | Placed trade: {new_row_limit_order}'
            }
            changelog = pd.concat([changelog, pd.DataFrame([new_row_changelog])], ignore_index=True)

    #Save updated into to CSVs        
    df_orders.to_csv(ORDER_FILE, index = False)
    df_buy_sell.to_csv(TRADE_FILE, index=False)
    changelog.to_csv(CHANGELOG, index = False)