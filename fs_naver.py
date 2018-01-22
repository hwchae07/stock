#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
#naver에서 가져와보자...

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bs
from pandas import Series, DataFrame
import pandas as pd
import re
import numpy as np

def get_fs_naver(ticker,item):
    fs_url = "http://finance.naver.com/item/main.nhn?code="+ticker
    req = Request(fs_url)
    html_text = urlopen(req).read()

    soup = bs(html_text,'lxml')
    d  = soup.find(text = item)
    d_ = d.find_all_next(class_="")

    data = d_[0:3]
    res = [float(v.text) for v in data]

    return(res)

def get_profile_naver(ticker):
    fs_url = "http://finance.naver.com/item/main.nhn?code="+ticker
    req = Request(fs_url)
    html_text = urlopen(req).read()

    soup = bs(html_text,'lxml')
    #네이버 페이지 오류....
    error_content = soup.find(class_="error_content")
    if bool(error_content):
        title = ["기업명","종목코드","현재주가","상장주식수","PER","PBR","배당수익률 (%)","당좌비율 (%)", "매출액 (억)","영업이익 (억)", "1년 수익률 (PBR 0.5)", "1년 수익률 (PBR 2)"]
        data = [np.NaN,np.NaN,np.NaN,np.NaN,np.NaN,np.NaN,np.NaN,np.NaN,np.NaN,np.NaN,np.NaN,np.NaN]
        info = DataFrame(data,index=title) #DataFrame형식으로 저장
        return info
    else:
        title = []
        data  = []


    t  = soup.find(text = "종목 시세 정보") #종목시세정보 가져온다
    t_ = t.find_all_next("dd")


    #종목 이름
    title.append("기업명")
    data.append(t_[1].text[3:].strip()) #기업명 저장
    #종목코드
    title.append("종목코드")
    data.append(ticker) #종목코드 저장

    ror = re.search('(\d+)(\s\w+)',t_[3].text[3:].replace(",","")) #정규표현식을 이용해서 현재주가만 골라옴
    price = float(ror.group(1))
    #현재 주가
    title.append("현재주가")
    data.append(price) #현재주가 저장

    number  = soup.find(text = "상장주식수")
    number_ = float(number.find_next("td").text.replace(',',''))
    #주식수
    title.append("상장주식수")
    data.append(number_) #상장주식수 저장

    per_table = soup.find(class_= "per_table") #per table 찾기
    #ETF 같은 애들은 per_table이 없음...
    if per_table is None:
        per = None
        pbr = None
        dvr = None
        IsEarningTable = False
    else:
        per = per_table.find_next("em",{"id" : "_per"}) #per 항목 가져옴
        pbr = per_table.find_next("em",{"id" : "_pbr"}) #pbr 항목 가져옴
        dvr = per_table.find_next("em", {"id": "_dvr"})  # 배당수익률 가져옴
        IsEarningTable = True

    # 상장된지 얼마 안된 기업의 경우 PER,PBR DVR이 없어서 0을 대신해서 넣는다. 나중에 None을 넣던지...
    if per is None:
        per = np.NaN
    else:
        per = float(per.text.replace(",",""))

    if pbr is None:
        pbr = np.NaN
    else:
        pbr = float(pbr.text)

    if dvr is None:
        dvr = np.NaN
    else:
        dvr = float(dvr.text)

    #per
    title.append("PER")
    data.append(per) #per 저장
    #pbr
    title.append("PBR")
    data.append(pbr) #pbr 저장
    #dividend ratio
    title.append("배당수익률 (%)")
    data.append(dvr) #배당수익률 저장


    #per_table = soup.find(class_= "per_table")
    #per = per_table.find_next("em",{"id" : "_per"})


    # 기업실적분석 테이블에 정보가 없을 경우 noinfo 가 있는 것을 이용해서
    # noinfo가 있을 경우에 quick ratio에 0을 넣는다... 나중에 None 넣던지...
    earning_table = soup.find(class_="noinfo")
    if IsEarningTable is False:
        quick = np.NaN
        sales = np.NaN
        oP = np.NaN
        roe1 = np.NaN
        roe2 = np.NaN
        roe3 = np.NaN
        debtRatio1 = np.NaN
        debtRatio2 = np.NaN
        debtRatio3 = np.NaN
    elif earning_table is None:
        # 당좌비율 찾기1
        # d  = soup.find(class_="h_th2 th_cop_anal15")
        d  = soup.find(text="당좌비율")
        d  = d.find_all_next("td")

        # 매출액 찾기
        # dd = soup.find(class_='h_th2 th_cop_comp7')
        dd = soup.find(text="매출액")
        dd = dd.find_all_next("td")

        # 영업이익 찾기
        # ddd = soup.find(class_='h_th2 th_cop_comp9')
        ddd = soup.find(text="영업이익")
        ddd = ddd.find_all_next("td")

        #roe1,2,3 찾기
        droe = soup.find(text="ROE(지배주주)")
        droe = droe.find_all_next("td")

        #debt ratio 1,2,3
        ddebt = soup.find(text="부채비율")
        ddebt = ddebt.find_all_next("td")

        try:
            roe1 = float(droe[0].text)
        except:
            roe1 = np.NaN
        try:
            roe2 = float(droe[1].text)
        except:
            roe2 = np.NaN
        try:
            roe3 = float(droe[2].text)
        except:
            roe3 = np.NaN


        try:
            debtRatio1 = float(ddebt[0].text)
        except:
            debtRatio1 = np.NaN
        try:
            debtRatio2 = float(ddebt[1].text)
        except:
            debtRatio2 = np.NaN
        try:
            debtRatio3 = float(ddebt[2].text)
        except:
            debtRatio3 = np.NaN

        try:
            quick = float(d[2].text)
        except:
            quick = np.NaN #나중에 None 넣던지...

        try:
            sales = float(re.search('\d+', dd[2].text.replace(',', '')).group())
        except:
            sales = np.NaN # 나중에 None 넣던지...

        try:
            oP = float(re.search('\d+', ddd[2].text.replace(',', '')).group())
        except:
            oP = np.NaN  # 나중에 None 넣던지...
    else:
        quick = np.NaN #나중에 None 넣던지...
        sales = np.NaN
        oP = np.NaN
        roe1 = np.NaN
        roe2 = np.NaN
        roe3 = np.NaN
        debtRatio1 = np.NaN
        debtRatio2 = np.NaN
        debtRatio3 = np.NaN

    roa1 = roe1 / (1 + debtRatio1 / 100)
    roa2 = roe2 / (1 + debtRatio2 / 100)
    roa3 = roe3 / (1 + debtRatio3 / 100)

    title.append("당좌비율 (%)")
    data.append(quick)  # 당좌비율 저장

    title.append("매출액 (억)")
    data.append(sales)  # 매출액 저장

    title.append("영업이익 (억)")
    data.append(oP)  # 영업이익 저장

    number_of_roa = 0
    if not np.isnan(roa1):
        number_of_roa = number_of_roa + 1
    if not np.isnan(roa2):
        number_of_roa = number_of_roa + 1
    if not np.isnan(roa3):
        number_of_roa = number_of_roa + 1

    if number_of_roa is 0:
        number_of_roa = np.NaN
    avgROA = (roa1 + roa2 + roa3) / number_of_roa

    #title.append("평균 ROA (%)")
    #data.append(avgROA)

    year = 3

    future_book = (price*number_/pbr)* (1 + avgROA/100 + dvr/100)**year
    halfPrice = future_book * 0.5 / number_
    doublePrice = future_book * 2 / number_
    earning_rate_half = (halfPrice / price)**(1/year)
    earning_rate_double = (doublePrice / price)**(1/year)
    #title.append("3년 뒤 주가 (PBR 0.5)")
    #data.append(halfPrice)
    #title.append("3년 뒤 주가 (PBR 2)")
    #data.append(doublePrice)
    title.append("1년 수익률 (PBR 0.5)")
    data.append(earning_rate_half)
    title.append("1년 수익률 (PBR 2)")
    data.append(earning_rate_double)

    #pd.set_option("display.column_space",20)
    info = DataFrame(data,index=title) #DataFrame형식으로 저장

    return info


#print(get_profile_naver("217810"))
#print(get_profile_naver("281410"))
#print( get_profile_naver("204210"))
#print (get_profile_naver("005930"))
#print (get_profile_naver("079440"))



#print (get_profile_naver("285130"))
#print (get_profile_naver("002460"))
#print (get_fs_naver("002460","당좌비율") )
#print (get_fs_naver("002460","주당배당금") )





"""
fs_url = "http://finance.naver.com/item/main.nhn?code=002460"
df = pd.read_html(fs_url)
req = Request(fs_url)
html_text = urlopen(req).read()

soup = bs(html_text,'html.parser')

item = "당좌비율"
#print(soup)
d  = soup.find(text=item)
print(d)
#부채비율 당좌비율 유보율만 찾아지고 나머지는 안찾아짐
#무엇이 문제인지 모르겠다.
#html 소스 봐서 "주당배당금(원)" 처럼 똑같이 적어서 넣어줘야된다 by무송
d_ = d.find_all_next("td",class_="")

data = d_[0:3]
res = [float(v.text) for v in data]
print (res)
"""
