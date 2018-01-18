#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
from fs_naver import *
from fs_sejong import *
import time
import pandas as pd
import numpy as np
import tabulate as tabulate
import glob

#get_fin_table_sejong_data(ticker, freq='a'):

ticker = "005930"
year = get_fin_table_sejong_data(ticker,'a')
quater = get_fin_table_sejong_data(ticker,'q')

#print (tabulate.tabulate(year, headers="keys", tablefmt='grid'))
print ()
#print (quater)

print (quater.iloc[1])
"""
for i in quater.index[1:]:
    quater[0][i] = quater[0][i].split(" ")[0]
    #print(table[0][i])
"""

#print (tabulate.tabulate(quater, headers="keys", tablefmt='grid'))
