#-*-coding:utf-8-*-

import numpy as np
import pandas as pd
from datetime import datetime

dane_spolki = pd.read_csv("c:\\Python27\\Projects\\gpw\\bzwbk.mst")

print dane_spolki.head()

przykladowy_czas = "19981201"
przeliczony_czas = date.strftime(przykladowy_czas, "%Y%m%d")
print przeliczony_czas 



