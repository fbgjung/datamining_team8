import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
# 삼성전자 005930.KS
# LG전자 066570.KS
# 삼성에스디에스 018260.KS
# SK하이닉스 000660.KS
# 삼성SDI 006400.KS
# LG디스플레이 034220.KS
pct_list = []
pct = []
pd.set_option('display.max_columns', None)
num=0
sel_date = [[],[],[],[],[],[]]
names = [{'name':'삼성전자','num':'005930.KS'},
        {'name':'LG전자','num':'066570.KS'},
        {'name':'삼성에스디에스','num':'018260.KS'},
        {'name':'SK하이닉스','num':'000660.KS'},
        {'name':'삼성SDI','num':'006400.KS'},
        {'name':'LG디스플레이','num':'034220.KS'}]
for stock in names:
    df1 = yf.download(stock['num'], start='2019-01-01',end='2019-12-31') ## 여기 날짜 수정해주세요!
    print('\n')
    print(stock['name'])
    for i in range(1,len(df1['Close'])):
        fluctuation_rate = (df1['Close'][i]-df1['Close'][i-1])/df1['Close'][i]*100
        if fluctuation_rate >= 3 or fluctuation_rate <= -3:
            print(df1.index[i],str(format((df1['Close'][i]-df1['Close'][i-1])/df1['Close'][i]*100,'.2f'))+'%')
            pct.append(str(format((df1['Close'][i]-df1['Close'][i-1])/df1['Close'][i]*100,'.2f')))
# 여기까지 3%이상 -3%이하 종가       
            sel_date[num].append(str(df1.index[i])[:10].replace('-',''))
    pct_list.append(pct)
    pct = []
    num+=1

num1 = 0
sel_date1 = [] # 해당 날짜 리스트
date_good = []
date_gg = []
for i in range(len(sel_date)):
    sel_date1.append(sel_date[i])
for i in range(len(sel_date1)):
    for j in range(len(sel_date1[i])):
        date_gg.append(sel_date1[i][j][4:6])
        date_gg.append(sel_date1[i][j][6:8])

    date_good.append(date_gg)
    date_gg = []

    
# print(len(date_good))

# 날짜 리스트 완성
    #------------------------------------------------------------------------------------------------------------------------------------------------
month_list = []
day_list = []
title_list = []
title1_list = []
title2_list = []
query = ['삼성전자 경제', 'LG전자 경제', '삼성에스디에스 경제', 'SK하이닉스 경제', '삼성SDI 경제', 'LG디스플레이 경제']  # 검색어
num2=0
for i in query:
    print('--------------------------'+i+'---------------------------')
    for j in range(0,len(date_good[num2]),2):
        month = int(date_good[num2][j])
        day = int(date_good[(num2)][j+1])-1
        if day == 0:
            month = month-1
            if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 0:
                day = 31
            elif month == 2: # 2월이 29일인 경우 바꿔주세요!
                day = 28
            elif month == 4 or month == 6 or month == 9 or month == 11:
                day = 30
        
        if month == 0:
            month = 12
        month_list.append(month)
        day_list.append(day)
        end_date = datetime(2019,month,day)  # 여기 년도 바꿔주세요!
        print('2019년 %s월'%month+' %s일'%day)
        base_url = 'https://search.naver.com/search.naver?where=news&sm=tab_opt'
        params = {
            'query': i,
            'ds': end_date.strftime('%Y.%m.%d'),
            'de': end_date.strftime('%Y.%m.%d'),
            'nso': 'so:r,p:from' + end_date.strftime('%Y%m%d') + 'to' + end_date.strftime('%Y%m%d'),
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
        }

        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        news_titles = soup.select('a.news_tit')

        for title in news_titles:
            print(title.get_text(strip=True)+' ')
            title2_list.append(title.get_text(strip=True)+' ')
        print('\n')
        title1_list.append(title2_list)
        title2_list = []
    title_list.append(title1_list)
    title1_list = []
    num2+=1

#-------------------------------------------------------------------------------------------------------------------------------------
#데이터 프레임 생성하기
data = [['회사명','날짜','등락률','뉴스 타이틀']]
data_info = []
for i in range(len(title_list)):
    for j in range(len(title_list[i])):
        for k in range(len(title_list[i][j])):
            data_info = []
            data_info.append(query[i])
            data_info.append(sel_date1[i][j])
            data_info.append(pct_list[i][j])
            data_info.append(title_list[i][j][k])
            data.append(data_info)
# 데이터프레임 생성
df = pd.DataFrame(data[1:], columns=data[0])

# 엑셀 파일로 저장
df.to_excel('2019.xlsx', index=False)