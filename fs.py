#!/usr/local/bin/python3
from fs_naver import *
from fs_sejong import *
import time
#import matplotlib.pyplot as plt

#print(get_profile_naver("002460"))

#print(get_fin_table_sejong_data("002460","a"))
#DataFrame 접근방법...


"""
df0 = get_profile_naver("002460")
df1 = get_profile_naver("005930") 
df = df0

df["1"] = df1

print(df.T)
"""


fin = open("kospi.csv","r")
lines = fin.readlines()

evtNumber = len(lines)
#evtNumber = 20

for ticker in range(evtNumber):
    print (ticker)
    if( (ticker % 20) == 0):
        progress = float(ticker)/float(evtNumber)*100
        print (str(progress)+"%")
    
    time.sleep(0.1)
    if(ticker == 0):
        tree = get_profile_naver(lines[ticker].strip())
    else:
        tree[ticker] = get_profile_naver(lines[ticker].strip())

tree.T.to_csv("./info_kospi.csv")

fin.close()




"""
table = get_fin_table_sejong_data("002460","a")

table[0][0] = "date"
for i in table.index[1:]:
    table[0][i] = table[0][i].split(" ")[0]
    #print(table[0][i])

#print (table)


#print(table.ix[0])

#print(table.info())
plt.plot(table[0][1:],table[1][1:])
plt.show()
"""
