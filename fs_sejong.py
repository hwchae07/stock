#!/usr/local/bin/python3
#아래 페이지 그대로 가져옴
#http://blog.naver.com/PostView.nhn?blogId=htk1019&logNo=221035489722&parentCategoryNo=&categoryNo=&viewDate=&isShowPopularPosts=false&from=postView

#urllib is a package that collect several modules for working with URLs
#urllib.request for opening and reading URLs
 

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bs
import pandas as pd

def get_html_sejong_fs(ticker, freq='a'):
    
    """
    종목코드를 입력하면 해당 종목의 연간 재무데이터 html 파일의 소스를 반환한다.
    :param ticker: 종목코드.
    :param freq: a : 연간재무데이터, q : 분기 재무데이터        
    """

    #연간 재무데이터 URL
    if freq=="a":
        fs_url = "http://www.sejongdata.com/business_include_fr/table_main0_bus_01.html?no="+ ticker + "&gubun=2"
    elif freq=='q':
        fs_url = "http://www.sejongdata.com/business_include_fr/table_main0_bus_02.html?no=" + ticker
    else:
        return None

    req = Request(fs_url,headers={'User-Agent': 'Mozilla/5.0'})
    html_text = urlopen(req).read()

    return(html_text)



"""
urllib.request.Request
This class is an abstraction of URL request

urllib.request.urlopen
open the URL

왜 굳이 이런 형식( urlopen(req)  )으로 input을 주는 이유를 잘 모름
"""

"""
#print( get_html_sejong_fs("005930",'a') )
#html형식으로 잔뜩 나온다... 봐도 잘 모르겠음...
"""

"""
#그래서 필요한 BeautifulSoup
#HTML을 파싱하는데 사용되는 Python 라이브러리라고 한다.

soup = bs( get_html_sejong_fs("005930","a") , "lxml")
print (soup.prettify())

#이런식으로 출력하면 좀 보기 편하다.
"""



def ext_fin_sejong_data(ticker, item, n, freq):
    """
            
    :param ticker: 종목코드
    :param item: html_text file에서 원하는 계정의 데이터를 가져혼다.
    :param n: 최근 몇 개의 데이터를 가져 올것인지
    :param freq: Y : 연간재무, Q : 분기재무
    :return: item의 과거 10년치 데이터
    """

    html_text = get_html_sejong_fs(ticker, freq)

    soup = bs(html_text, 'lxml')
    d = soup.find(text=item)
    d_ = d.find_all_next(class_="bus_board_txt1")

    #계정의 과거 데이터 수 : 연간재무정보 또는 재무비율 은 10 개 분기재무정보는 12개
    ndata = 12 if freq == "q" else 10

    data = d_[(ndata-n):ndata]
    v = [v.text for v in data]

    return(v)


"""
soup = bs( get_html_sejong_fs("005930","a") , "lxml")
d  = soup.find(text = "매출액")
d_ = d.find_all_next(class_="bus_board_txt1")
#왜 class가 아니라 class_ 인지 모르겠다.
data = d_[0:10]
v = [v.text for v in data]
#.text는 html안에 있는 값을 가져와주는 역할인듯...
print (v)
"""


def get_fin_table_sejong_data(ticker,freq='a'):
    """
    :param ticker : 종목코드
    :return: 재무데이터 테이블 전체를 반환한다.
    """
    try :
        # 연간 재무데이터 테이블을 한꺼번에 가져옵니다.
        if freq =='a':
            fs_url = "http://www.sejongdata.com/business_include_fr/table_main0_bus_01.html?no="+ ticker + "&gubun=2"
            df = pd.read_html(fs_url, encoding='utf-8')[1]
            df = df.T

        # 분기 재무데이터 테이블을 한꺼번에 가져옵니다.
        elif freq=='q':
            fs_url = "http://www.sejongdata.com/business_include_fr/table_main0_bus_02.html?no=" + ticker
            df = pd.read_html(fs_url, encoding='utf-8')
        else :
            fs_url = None
            df = None
    except AttributeError as e:
        return None

    return df



"""
pandas 의 Series는 1차원 데이터 분석하기에 효과적
pandas 의 DataFrame은 2차원 데이터를 분석하기에 효과적

pandas.read_html
Read html tables into a list of DataFrame objects.
"""
"""
ticker = "005930"
fs_url = "http://www.sejongdata.com/business_include_fr/table_main0_bus_01.html?no="+ ticker + "&gubun=2"
df = pd.read_html(fs_url, encoding='utf-8')
#print (df)
print(df[0])
print(df[4])
#df[1] : 매출액 등등...table
#df[4] : 재무비율 table
"""
#예제1. 연간 재무데이터 전부 다 긁기
#print( get_fin_table_sejong_data("005930") )

#예제2. 삼성전자 매출액 과거 최근 3개분기 데이터 가져오기
#print ( ext_fin_sejong_data("005930","매출액", 3, "q") )
