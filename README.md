# Instructions on usage
Place orders by using a order csv file from the Order_files folder such as "xx_order.csv" in the format of:

Date(YYYY-MM-DD),Action(buy/sell),TriggerPrice,Number of units,Ticker,Status

**The formats and column names should be strictly followed to avoid the order being skipped or imported incorrectly. i.e. Please do not change any column names yourself and do not use the wrong data type, formatting, or include extra spaces.**
<br>

A program will check for whether the order is executed, and if it is, automatically place a market order in this format:

Date(YYYY-MM-DD),Action(buy/sell),Number of units,Ticker

To analyze your portfolio, just directly take the files from the Completed_trades folder. e.g. "xx_trades.csv".

The "status" of the order will be changed to completed and the history of such a automatic order will also be added into changelog once a order is complete. The changelog is there to help verify what orders are executed in case there are any situations where the program is buggy and placed some wrong orders.
<br>

**To add more teams:**<br>
To add CSV files to be processed, it must be added to the two lists at the very start of the program (make sure the index is matching). It also has to be added in the Github actions program under "Commit and push changes" to make sure any changes made by the order program is properly saved and updated.

The current available order types under Action(mb/ms/lb/ls/sl/sb):

1. marketbuy:<br>
Simple order to buy at next day's opening price

2. marketsell:

Simple order to sell at next day's opening price

3. limitbuy:

Is the limit buy order, if price drops below trigger price then the selected number of stocks will be bought automactically. Compare with prev day low

4. limitsell:

Is the limit sell order, if price reaches above the trigger price then the selected number of stocks will be sold automatically. Compare with prev day high

5. stoploss:

Is the stoploss order, is prices reach below the trigger price, then the number of stocks selected will be sold automatically. Compare with prev day low

6. stopbuy:

Is the stop buy order, if prices reach above the trigger price, then the number of stocks selected will be bought automatically. Compare with prev day high

**Please remember to use the full names when placing orders, i.e. write limitsell not ls**

Notes:
1. Currently, the program has yet to be tested properly so may have a low tolerenance for user input error and any formats that are non-standard will likely result in a order just being skipped. Please follow the proper expected formatting requirements
2. The program executes at 11am (hkt) everyday and checks for yesterday's prices. This is to ensure that yfinance has all the data for all the markets around the world. Orders placed on the date will be ingored until the next day. (e.g. A order placed on Jan 10 will only be treated as valid when the program is checking for Jan 11 orders)
3. All currencies are in the local currency, when placing orders just use the local market currency. **No** currency conversion of any kind is required (e.g. traded on HKEX just directly use nominal value in HKD)


Current Teams & files
1. Technology
2. Healthcare
3. Financials
4. Consumer Discretionary
5. Consumer Staples
6. Industrials
7. Energy
8. Utilities
9. Materials
10. Telecommunications
11. Real Estate

Common Q&A:
1. 

Q: I placed my order and it should have executed but the trade is not shown in my trade file?<br>
A: Note that the trade file is only updated at around 11am HKT the next day for each trading day, so if you just wait a day it may show up. If it still does not show up, please check your formatting, any invalid data types or extra spaces may have triggered an error which will cause your order to be noted as invalid<br>
e.g. Invalid date: 10/10/2025 | Correct date: 2025-10-10<br>
e.g. Invalid formatting: ...buy,  100,... | Correct formatting: ...buy,100,... (No extra spaces)



# Documentation for program (for future programmers)
All files used in the program are initialized and assigned in the first 3 lines of code
