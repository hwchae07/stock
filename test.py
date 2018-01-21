#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
from fs_naver import *
from fs_sejong import *
import time
import pandas as pd
import numpy as np
import tabulate as tabulate
import matplotlib.pyplot as plt

#get_fin_table_sejong_data(ticker, freq='a'):

ticker = "005490"
year = get_fin_table_sejong_data(ticker,'a')
quater = get_fin_table_sejong_data(ticker,'q')

year["ROE"] = year["순이익"]/year["자본총계"] * 100
year["ROA"] = year["순이익"]/year["자산총계"] * 100
print (tabulate.tabulate(year, headers="keys", tablefmt='grid'))
print ()

plt.plot(year["ROE"])
plt.ylabel("ROE")
plt.xlabel("연도")
plt.show()
#print (quater)

#print (quater.iloc[1])
"""
for i in quater.index[1:]:
    quater[0][i] = quater[0][i].split(" ")[0]
    #print(table[0][i])
"""

#print (tabulate.tabulate(quater, headers="keys", tablefmt='grid'))
