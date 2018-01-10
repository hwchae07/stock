#!/usr/local/bin/python3
from fs_naver import *
from fs_sejong import *
import time
import random
import pandas as pd
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

    evtNumber = len(lines)
    numberGroup = int(evtNumber/100+1)
    groupRange = range((groupIndex-1)*100,groupIndex*100)
    if(evtNumber < groupIndex*100):
        groupRange = range((groupIndex-1)*100,evtNumber)
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



#fs_to_csv("kospi",5)
#fs_to_csv("kosdaq",12)


pd.set_option('expand_frame_repr',False)
tree = pd.read_csv("./info_kospi_1.csv",encoding='cp949').T
for i in range(1):
    fileAdd = "./info_kospi_%d.csv"%(i+2)
    treeAdd = pd.read_csv(fileAdd,encoding='cp949').T
    tree = pd.concat([tree,treeAdd],axis=1).T


#tree1 = pd.read_csv("./info_kospi_1.csv",encoding='cp949').T
#tree2 = pd.read_csv("./info_kospi_2.csv",encoding='cp949').T
#tree = pd.concat([tree1,tree2],axis=1).T



print (tree[(abs(tree["PBR"]-0.7)<0.3) & (abs(tree["PER"]-7)<7) ])
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
