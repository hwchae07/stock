#!/usr/local/bin/python3
#-*- coding: utf-8 -*- 
#naver에서 가져와보자...

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bs
from pandas import Series, DataFrame
import pandas as pd
import re

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
    t  = soup.find(text = "종목 시세 정보") #종목시세정보 가져온다
    t_ = t.find_all_next("dd")

    title = []
    data  = []
    
    #종목 이름
    title.append("기업명")
    data.append(t_[1].text[3:].strip()) #기업명 저장
    #종목코드
    title.append("종목코드")
    data.append(ticker) #종목코드 저장

    ror = re.search('(\d+)(\s\w+)',t_[3].text[3:].replace(',','')) #정규표현식을 이용해서 현재주가만 골라옴
    #현재 주가
    title.append("현재주가")
    data.append(float(ror[1])) #현재주가 저장

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
        per = 0
    else:
        per = float(per.text.replace(",",""))
        
    if pbr is None:
        pbr = 0
    else:
        pbr = float(pbr.text)
        
    if dvr is None:
        dvr = 0
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
        quick = 0
    elif earning_table is None:
        d  = soup.find(class_="h_th2 th_cop_anal15")
        d  = d.find_next(text="당좌비율")  # 당좌비율 찾기1
        d  = d.find_all_next("td")
        try:
            quick = float(d[2].text)
        except:
            quick = 0 #나중에 None 넣던지...
    else:
        quick = 0 #나중에 None 넣던지...
        
    title.append("당좌비율 (%)")
    data.append(quick) #당좌비율 저장

    #pd.set_option("display.column_space",20)
    info = DataFrame(data,index=title) #DataFrame형식으로 저장
    
    return info


#print(get_profile_naver("009410"))
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

