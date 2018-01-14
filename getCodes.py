import pandas as pd
import numpy as np
import requests

from bs4 import BeautifulSoup
from io import BytesIO


def stock_master(index):
    # 0 for all, 1 for Kospi, 2 for Kosdaq, 3 for Konex

    MarketType = {0: '', 1: 'stockMkt', 2: 'kosdaqMkt', 3: 'konexMkt'}
    dummy = MarketType[index]
    url = 'http://kind.krx.co.kr/corpgeneral/corpList.do'
    data = {
        'method':'download',
        'orderMode':'1',           # 정렬컬럼
        'orderStat':'D',           # 정렬 내림차순
        'marketType' : 'stockMkt',
        'searchType':'13',         # 검색유형: 상장법인
        'fiscalYearEnd':'all',     # 결산월: 전체
        'location':'all',          # 지역: 전체
    }

    r = requests.post(url, data=data)
    f = BytesIO(r.content)
    dfs = pd.read_html(f, header=0, parse_dates=['상장일'])
    df = dfs[0].copy()

    # 숫자를 앞자리가 0인 6자리 문자열로 변환
    df['종목코드'] = df['종목코드'].astype(np.str)
    df['종목코드'] = df['종목코드'].str.zfill(6)
    return df


# df_master = stock_master(1)
# print(df_master['종목코드'])