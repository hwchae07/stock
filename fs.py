#!/usr/local/bin/python3
#-*- coding: utf-8 -*- 
from fs_naver import *
from fs_sejong import *
import time
import random
import pandas as pd
import numpy as np
import tabulate as tabulate
import glob
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


def fs_to_csv(marketName="kospi",groupIndex=1):
    fin = open(marketName+".csv","r")
    lines = fin.readlines()
    fin.close()
    howMany = 10
    evtNumber = len(lines)
    numberGroup = int(evtNumber/howMany+1)
    groupRange = range((groupIndex-1)*howMany,groupIndex*howMany)
    if(evtNumber < groupIndex*howMany):
        groupRange = range((groupIndex-1)*howMany,evtNumber)
    if(numberGroup < groupIndex):
        print ("No data...")
        return 0
    print (groupRange)

    for ticker in groupRange:
        print (ticker)

        time.sleep(0.5)
        if(ticker == groupRange[0]):
            tree = get_profile_naver(lines[ticker].strip())
            tree.columns.values[0] = ticker
        else:
            tree[ticker] = get_profile_naver(lines[ticker].strip())


    tree.T.to_csv("./info_"+marketName+"_%d.csv" % groupIndex)
    print("save "+marketName+" is done...")

    return 1


for i in range(1, 10):
    try:
        fs_to_csv("kosdaq", i)
    except:
        try:
            fs_to_csv("kosdaq", i)
        except:
            print('%d-th kosdaq data importing fail' % i)
            continue

for i in range(1, 10):
    try:
        fs_to_csv("kospi", i)
    except:
        try:
            fs_to_csv("kospi", i)
        except:
            print('%d-th kospi data importing fail' % i)
            continue


#get number of files
nKosdaq = len(glob.glob("info_kosdaq*"))
nKospi = len(glob.glob("info_kospi*"))


pd.set_option('expand_frame_repr',False)
tree = pd.DataFrame()
# tree = pd.read_csv("./info_kospi_1.csv",encoding='cp949').T
for i in range(nKospi):
    fileAdd = "./info_kospi_%d.csv"%(i+1)
    treeAdd = pd.read_csv(fileAdd,encoding='cp949').T
    tree = pd.concat([tree,treeAdd],axis=1)

for i in range(nKosdaq):
    fileAdd = "./info_kosdaq_%d.csv"%(i+1)
    treeAdd = pd.read_csv(fileAdd,encoding='cp949').T
    tree = pd.concat([tree,treeAdd],axis=1)

tree = tree.T

tree['시가총액 (억)'] = tree['상장주식수'] * tree['현재주가'] / 10**8


# 조건 추가
cond = pd.DataFrame()
cond["PBR"] = (tree["PBR"] > 0.4) & (tree["PBR"] < 1.2)
cond["PER"] = (tree["PER"]>3) &  (tree["PER"]<15)
cond["배당수익률"] = tree['배당수익률 (%)']>2
cond["당좌비율"] = tree['당좌비율 (%)']>80

# 조건에 and 연산
test = cond["PBR"]
for key in cond.keys():
    test = test & cond[key]

# 필터링
result = tree[test]

# 종목코드를 6자리로 만들기 위한 코드 두 줄
result.loc[:, ('종목코드')] = result.loc[:, ('종목코드')].astype(np.str)
result.loc[:, ('종목코드')] = result.loc[:, ('종목코드')].str.zfill(6)

result['PSR'] = result['시가총액 (억)'] / result['매출액 (억)']
result['POR'] = result['시가총액 (억)'] / result['영업이익 (억)']

# print(screen4['종목코드'])
print(tabulate.tabulate(result, headers="keys", tablefmt='grid'))
result.to_csv("./screen.csv")
#print (tree.T)


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
