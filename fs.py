#!/usr/local/bin/python3
#-*- coding: utf-8 -*- 
from fs_naver import *
from fs_sejong import *
import time
import pandas as pd
import numpy as np
import tabulate as tabulate
import glob
from getCodes import *
#import matplotlib.pyplot as plt

#print(get_profile_naver("002460"))

#print(get_fin_table_sejong_data("002460","a"))
#DataFrame 접근방법...


def takeDataFromNaver(doOrNot):  # 이 안에 fs_to_csv 가 정의되어 있음
    """
    :param doOrNot : 실행 여부
    :return: 없음. 모든 종목들의 csv 파일들이 폴더 안에 만들어짐.
    """
    if not doOrNot:             # doOrNot이 False면 실행하지 마!
        return

    def fs_to_csv(marketName="kospi", groupIndex=1):
        """
        :param marketName : 코스피냐 코스닥이냐
        :param groupIndex : 몇 번째 그룹의 종목들을 가져올 것이냐. 한 종목에 150개
        :return: 없음. csv 파일 하나가 폴더 안에 만들어짐.
        """
        if marketName == 'kospi':
            list = stock_master(1)['종목코드']
        elif marketName == 'kosdaq':
            list = stock_master(2)['종목코드']

        lines = list
        howMany = 150
        evtNumber = len(lines)
        numberGroup = int(evtNumber / howMany + 1)
        groupRange = range((groupIndex - 1) * howMany, groupIndex * howMany)
        if (evtNumber < groupIndex * howMany):
            groupRange = range((groupIndex - 1) * howMany, evtNumber)
        if (numberGroup < groupIndex):
            print("No data...")
            return 0
        print(groupRange)
        for ticker in groupRange:
            print(ticker)
            time.sleep(0.5)
            if ticker == groupRange[0]:
                tree = get_profile_naver(lines[ticker].strip())
                tree.columns.values[0] = ticker
            else:
                tree[ticker] = get_profile_naver(lines[ticker].strip())
        tree.T.to_csv("./info_" + marketName + "_%d.csv" % groupIndex)
        print("save " + marketName + " is done...")
        return
    # get kosdaq information from Naver

    for i in range(1, 10):
        try:
            fs_to_csv("kosdaq", i)
        except:
            try:
                fs_to_csv("kosdaq", i)
            except:
                print('%d-th kosdaq data importing fail' % i)
                continue

    # get kospi information from Naver
    for i in range(1, 10):
        try:
            fs_to_csv("kospi", i)
        except:
            try:
                fs_to_csv("kospi", i)
            except:
                print('%d-th kospi data importing fail' % i)
                continue

    return


def makeDataFrame():      # csv에 나눠서 저장된 정보를 하나의 DataFrame에 합체!
    """
    :return: 모든 종목들의 csv 파일들의 정보를 포함하는 DataFrame.
    """
    #get number of files
    nKosdaq = len(glob.glob("info_kosdaq*"))
    nKospi = len(glob.glob("info_kospi*"))
    pd.set_option('expand_frame_repr', False)
    tree = pd.DataFrame()
    for i in range(nKospi):
        fileAdd = "./info_kospi_%d.csv"%(i+1)
        treeAdd = pd.read_csv(fileAdd, encoding='cp949').T
        tree = pd.concat([tree, treeAdd], axis=1)
    for i in range(nKosdaq):
        fileAdd = "./info_kosdaq_%d.csv"%(i+1)
        treeAdd = pd.read_csv(fileAdd, encoding='cp949').T
        tree = pd.concat([tree, treeAdd], axis=1)
    tree = tree.T
    tree['시가총액 (억)'] = tree['상장주식수'] * tree['현재주가'] / 10**8
    tree = tree.drop('Unnamed: 0', 1)
    return tree


# 네이버로부터 fs_to_csv 함수를 사용해서 csv를 만듦. 150개씩 끊어서...
# csv를 만들거면 true, 이미 csv 파일이 있으면 false~~!
takeDataFromNaver(False)

# 만든 csv 파일들을 합쳐서 DataFrame으로 만듦
fullList = makeDataFrame()

# 원하는 지표 생성  (사실이건 makeDataFrame에서 해야할 것 같지만.. 가시성을 위해 여기 둔다)
fullList.loc[:, 'PSR'] = fullList['시가총액 (억)'] / fullList['매출액 (억)']
fullList.loc[:, 'POR'] = fullList['시가총액 (억)'] / fullList['영업이익 (억)']
fullList.loc[:, 'ROE'] = fullList['PBR'] / fullList['PER'] *100

# 필터링 할 조건 추가
cond = pd.DataFrame()
cond["PBR 조건"] = (fullList["PBR"] > 0.4) & (fullList["PBR"] < 1.2)
#cond["PER 조건"] = (fullList["PER"] > 3) & (fullList["PER"] < 15)
cond["배당수익률 조건"] = fullList['배당수익률 (%)'] > 1
cond["당좌비율 조건"] = fullList['당좌비율 (%)'] > 80
cond["POR 조건"] = fullList['POR'] < 10

# 각각의 조건에 and 연산
fullCondition = cond[cond.columns[0]]  # 첫 번째 열로 fullCondition 초기화
for key in cond.keys():
    fullCondition = fullCondition & cond[key]

# 필터링
result = fullList[fullCondition]

# 종목코드를 6자리로 만들기 위한 코드
code = result['종목코드'].astype(np.str)
result.loc[:, '종목코드'] = code.str.zfill(6)

# output에 출력
print(tabulate.tabulate(result, headers="keys", tablefmt='grid'))

# csv로 저장
result.to_csv("./screen.csv")

# 갯수 출력
print(len(result))

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
