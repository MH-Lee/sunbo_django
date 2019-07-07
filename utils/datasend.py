import bs4
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import os, sys, glob
import datetime

start_path = os.getcwd()
proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onside.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
import django
print("사용자 모델 불러오기")
from django.contrib.auth.models import User
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from information.models import Dart, Rescue
from news.models import (InvestNews,
                        LPCompany,
                        MainCompany,
                        Portfolio,
                        Professor)

def remove_tag(data):
    try:
        soup = BeautifulSoup(data, "html.parser")
        ret = soup.find('a').text.strip()
    except AttributeError:
        ret = data
    except TypeError:
        ret = None
    return ret

def get_url(data):
    try:
        soup = BeautifulSoup(data, "html.parser")
        ret = soup.find('a')
        url = ret['href']
    except AttributeError:
        url = None
    except TypeError:
        url = None
    return url

def dart_send():
    data = pd.read_excel('./data/dart.xlsx')
    data['뉴스제목'] = data['관련뉴스기사'].apply(lambda x:remove_tag(x))
    data['뉴스URL'] = data['관련뉴스기사'].apply(lambda x:get_url(x))
    data['문서내용'] = data['문서내용'].apply(lambda x:get_url(x))
    data['회사코드'] = data['회사코드'].apply(lambda x:str(x).zfill(6))
    data[data['공시대상회사'] == '후이즈']['회사코드']
    index = np.where(data['공시대상회사'] == '후이즈')
    for i in index[0]:
        print(i)
        data.loc[i,'회사코드'] = '297120'
    data1 = data[['공시대상회사', '회사코드', '공시접수일자', '타법인명', '문서내용', '뉴스제목', '뉴스URL']]
    data1.sort_values(by=['공시접수일자'], inplace=True)
    dart_list = []
    for i in range(data1.shape[0]):
        print(i)
        company_name = data1.iloc[i,0]
        ticker = data1.iloc[i,1]
        date = data1.iloc[i,2]
        another_name = data1.iloc[i,3]
        contents = data1.iloc[i,4]
        news_title = str(data1.iloc[i,5])
        news_url = str(data1.iloc[i,6])
        if news_url == 'nan':
            news_url = None
        writer = User.objects.get(username='admin')
        dart_obj = Dart(company_name=company_name, ticker=ticker,\
                        date=date, another_name=another_name, contents=contents,\
                        news_title=news_title, news_url=news_url, writer=writer)
        dart_list.append(dart_obj)
    Dart.objects.bulk_create(dart_list)

def invest_news_send():
    data = pd.read_excel('./data/invest_news.xlsx')
    data.sort_values(by=['날짜'], inplace=True)
    data['뉴스URL'] = data['뉴스제목'].apply(lambda x:get_url(x))
    data['뉴스제목'] = data['뉴스제목'].apply(lambda x:remove_tag(x))
    invest_list = []
    for i in range(data.shape[0]):
        media = data.iloc[i,0],
        date =  data.iloc[i,2].strftime('%Y-%m-%d'),
        news_title = data.iloc[i,1],
        news_url = data.iloc[i,3],
        writer = User.objects.get(username='admin')
        invest_obj = InvestNews(media=media, date=date, news_title=news_title,\
                                news_url=news_url, writer=writer)
        invest_list.append(invest_obj)
    InvestNews.objects.bulk_create(invest_list)
    print('invest_news 업로드')


def LP_company_send():
    data = pd.read_excel('./data/invest_news.xlsx')
    data.sort_values(by=['날짜'], inplace=True)
    data['뉴스URL'] = data['뉴스제목'].apply(lambda x:get_url(x))
    data['뉴스제목'] = data['뉴스제목'].apply(lambda x:remove_tag(x))
    invest_list = []
    for i in range(data.shape[0]):
        media = data.iloc[i,0],
        date =  data.iloc[i,2].strftime('%Y-%m-%d'),
        news_title = data.iloc[i,1],
        news_url = data.iloc[i,3],
        writer = User.objects.get(username='admin')
        invest_obj = InvestNews(media=media, date=date, news_title=news_title,\
                                news_url=news_url, writer=writer)
        invest_list.append(invest_obj)
    InvestNews.objects.bulk_create(invest_list)
    print('invest_news 업로드')
