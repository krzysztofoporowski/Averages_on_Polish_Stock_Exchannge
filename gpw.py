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
    else:
        return 0

#end of functions section

#data loading from the MST files
stock_data = pd.read_csv("c:\\Python27\\Projects\\gpw\\bzwbk.mst")

stock_data["<DTYYYYMMDD>"] = stock_data["<DTYYYYMMDD>"].apply(convert_date)
stock_data.columns = ["Stock", "Date", "Open", "High", "Low", "Close", "Volume"]
stock_data.set_index("Date",inplace = True)

#calculating moving averages
fast_ma_period = 5
slow_ma_period = 21

stock_data["Fast_MA"] = stock_data["Close"].rolling(window = fast_ma_period).mean()
stock_data["Slow_MA"] = stock_data["Close"].rolling(window = slow_ma_period).mean()

#removing all the NaN from the Slow_Ma and Fast_MA
stock_data_without_nan = stock_data[stock_data["Slow_MA"].notnull()]

#generating signals
stock_data_without_nan["Signal"] = stock_data_without_nan.apply(generate_signal, axis = 1)

print stock_data_without_nan.head()
print stock_data_without_nan.tail()



