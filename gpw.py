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
    if row["Signal-1"] == 1 and row["Signal-2"] == -1:
        return (row["Open"] * -1)
    elif row["Signal-2"] == 1 and row["Signal-1"] == -1:
        return row["Open"]

#end of functions section

#data loading from the MST files
stock_data = pd.read_csv("c:\\Python27\\Projects\\gpw\\bzwbk.mst")

stock_data["<DTYYYYMMDD>"] = stock_data["<DTYYYYMMDD>"].apply(convert_date)
stock_data.columns = ["Stock", "Date", "Open", "High", "Low", "Close", "Volume"]
stock_data.set_index("Date",inplace = True)

#calculating moving averages
fast_ma_period = 50
slow_ma_period = 100

stock_data["Fast_MA"] = stock_data["Close"].rolling(window = fast_ma_period).mean()
stock_data["Slow_MA"] = stock_data["Close"].rolling(window = slow_ma_period).mean()

#removing all the NaN from the Slow_Ma and Fast_MA
stock_data_without_nan = stock_data[stock_data["Slow_MA"].notnull()]

#generating signals
stock_data_without_nan["Signal"] = stock_data_without_nan.apply(generate_signal, axis = 1)
stock_data_without_nan["Signal-1"] = stock_data_without_nan["Signal"].shift(1)
stock_data_without_nan["Signal-2"] = stock_data_without_nan["Signal-1"].shift(1)
stock_data_without_nan = stock_data_without_nan[stock_data_without_nan["Signal-2"].notnull()]
stock_data_without_nan["Buy_price"] = stock_data_without_nan.apply(buy_stock, axis = 1)
stock_data_without_nan["Stock_number"] = stock_data_without_nan[stock_data_without_nan["Buy_price"].notnull()].apply(lambda v: int(1000 / v["Buy_price"]), axis = 1)
stock_data_without_nan["Transaction_value"] = stock_data_without_nan["Buy_price"] * stock_data_without_nan["Stock_number"].abs() - stock_data_without_nan["Buy_price"] * stock_data_without_nan["Stock_number"].abs() * 0.0039


print stock_data_without_nan[stock_data_without_nan["Buy_price"].notnull()].tail()
print stock_data_without_nan["Transaction_value"].sum()
#print stock_data_without_nan[stock_data_without_nan["Signal"] == 1]
#print stock_data_without_nan.tail(100)



