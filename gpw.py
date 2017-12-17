#-*-coding:utf-8-*-

import numpy as np
import pandas as pd
from datetime import datetime

#functions section

def convert_date(row):
    #Function converts the long value from the original <DTYYYYMMDD> column representing date time from the MST file to the
    #date object.
    return datetime.strptime(str(row),"%Y%m%d").date()

def generate_signal(row):
    #Function returns 1 if the signal has been generated. The signal is defined as the Fast MA crossing from below the Slow MA
    if row["Fast_MA"] > row["Slow_MA"]:
        return 1
    elif row["Slow_MA"] > row["Fast_MA"]:
        return -1
def buy_stock(row):
    #Function calculates if buy or not. The budget for one transaction is 1000 PLN.
    if row["Signal_1"] == 1 and row["Signal_2"] == -1:
        return (row["Open"] * -1)
    elif row["Signal_2"] == 1 and row["Signal_1"] == -1:
        return row["Open"]

#end of functions section

budget = 1000 #PLN
transaction_fee = 0.0039 # wich means 0.39%. Adjust to your broker's transaction percentage

results = pd.DataFrame(columns=["Stock","Fast_MA","Slow_MA","Return"])
indeks = 0

fast_range = 10

#data loading from the MST files
for i in range (5,fast_range):
    print i
    for j in range (6, fast_range + 1):
        stock_data = pd.read_csv("c:\\Python27\\Projects\\gpw\\bzwbk.mst")

        stock_data["<DTYYYYMMDD>"] = stock_data["<DTYYYYMMDD>"].apply(convert_date)
        stock_data.columns = ["Stock", "Date", "Open", "High", "Low", "Close", "Volume"]
        stock_data.set_index("Date",inplace = True)

        #calculating moving averages
        fast_ma_period = i
        slow_ma_period = j

        stock_data["Fast_MA"] = stock_data["Close"].rolling(window = fast_ma_period).mean()
        stock_data["Slow_MA"] = stock_data["Close"].rolling(window = slow_ma_period).mean()

        #removing all the NaN from the Slow_Ma and Fast_MA
        stock_data_without_nan = stock_data[stock_data["Slow_MA"].notnull()]

        #generating signals
        stock_data_without_nan = stock_data_without_nan.assign(Signal=stock_data_without_nan.apply(generate_signal, axis = 1))

        #building history of signals
        stock_data_without_nan = stock_data_without_nan.assign(Signal_1 = stock_data_without_nan["Signal"].shift(1))
        stock_data_without_nan = stock_data_without_nan.assign(Signal_2 = stock_data_without_nan["Signal_1"].shift(1))

        #removing all NaNs
        stock_data_without_nan = stock_data_without_nan[stock_data_without_nan["Signal_2"].notnull()]

        #defining the price of transaction. Price with "minus" defines buy transaction, price with "plus" defines sell transaction
        stock_data_without_nan.loc[:,"Buy_price"] = stock_data_without_nan.apply(buy_stock, axis = 1)

        #calculating the number of stocks to be bought. The budget is 1000 PLN
        stock_data_without_nan.loc[:,"Stock_number"] = stock_data_without_nan[stock_data_without_nan["Buy_price"].notnull()].apply(lambda v: int(budget / v["Buy_price"]), axis = 1)

        #calculate the transaction value, including the transaction fee
        stock_data_without_nan.loc[:,"Transaction_value"] = stock_data_without_nan["Buy_price"] * stock_data_without_nan["Stock_number"].abs() - stock_data_without_nan["Buy_price"] * stock_data_without_nan["Stock_number"].abs() * transaction_fee
        row = ["BZWBK",fast_ma_period, slow_ma_period,stock_data_without_nan["Transaction_value"].sum()]
        results.loc[indeks] = row
        #print results.tail()
        indeks = indeks +1
        # nie działa, trzeba zrobić czyszczenie stock_data

print results[results["Return"].max()]
results.to_csv("wynik.csv")




