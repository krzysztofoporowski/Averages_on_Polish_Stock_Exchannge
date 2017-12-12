#-*-coding:utf-8-*-

import numpy as np
import pandas as pd
from datetime import datetime

#functions section

def convert_date(row):
    #Function converts the long value from the original <DTYYYYMMDD> column representing date time from the MST file to the
    #date object.
    return datetime.strptime(str(row),"%Y%m%d").date()

#end of functions section

#data loading from the MST files
stock_data = pd.read_csv("c:\\Python27\\Projects\\gpw\\bzwbk.mst")

stock_data["<DTYYYYMMDD>"] = stock_data["<DTYYYYMMDD>"].apply(convert_date)
stock_data.columns = ["Stock", "Date", "Open", "High", "Low", "Close", "Volume"]
stock_data.set_index("Date",inplace = True)

print stock_data.head()



