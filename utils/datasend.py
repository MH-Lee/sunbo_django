import bs4
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import os, sys, glob
import datetime

start_path = os.getcwd()
proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onspace.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
import django
print("사용자 모델 불러오기")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.contrib.auth.models import User
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
        media = data.iloc[i,0]
        date =  data.iloc[i,2].strftime('%Y-%m-%d')
        news_title = data.iloc[i,1]
        news_url = data.iloc[i,3]
        writer = User.objects.get(username='admin')
        invest_obj = InvestNews(media=media, date=date, news_title=news_title,\
                                news_url=news_url, writer=writer)
        invest_list.append(invest_obj)
    InvestNews.objects.bulk_create(invest_list)
    print('invest_news 업로드')

def LP_company_send():
    data = pd.read_excel('./data/LPcompany.xlsx')
    data.sort_values(by=['날짜'], inplace=True)
    data['뉴스URL'] = data['뉴스제목'].apply(lambda x:get_url(x))
    data['뉴스제목'] = data['뉴스제목'].apply(lambda x:remove_tag(x))
    lpc_list = []
    for i in range(data.shape[0]):
        category = data.iloc[i,0]
        company_name  = data.iloc[i,1]
        news_title = data.iloc[i,2]
        media = data.iloc[i,3]
        date =  data.iloc[i,4].strftime('%Y-%m-%d'),
        news_url = data.iloc[i,5]
        writer = User.objects.get(username='admin')
        lpc_obj = LPCompany(category=category, company_name=company_name, media=media, date=date,\
                                news_title=news_title, news_url=news_url, writer=writer)
        lpc_list.append(lpc_obj)
    LPCompany.objects.bulk_create(lpc_list)
    print('LP기업 업로드')

def main_company_send():
    data = pd.read_excel('./data/main_company.xlsx')
    data.sort_values(by=['날짜'], inplace=True)
    data['뉴스URL'] = data['뉴스제목'].apply(lambda x:get_url(x))
    data['뉴스제목'] = data['뉴스제목'].apply(lambda x:remove_tag(x))
    main_list = []
    for i in range(data.shape[0]):
        category = data.iloc[i,0]
        company_name  = data.iloc[i,1]
        news_title = data.iloc[i,2]
        media = data.iloc[i,3]
        date =  data.iloc[i,4].strftime('%Y-%m-%d')
        news_url = data.iloc[i,5]
        writer = User.objects.get(username='admin')
        main_obj = MainCompany(category=category, company_name=company_name, media=media, date=date,\
                                news_title=news_title, news_url=news_url, writer=writer)
        main_list.append(main_obj)
    MainCompany.objects.bulk_create(main_list)
    print('Main기업 업로드')

def protfolio_send():
    data = pd.read_excel('./data/Portfolio.xlsx')
    data.sort_values(by=['날짜'], inplace=True)
    data['뉴스URL'] = data['뉴스제목'].apply(lambda x:get_url(x))
    data['뉴스제목'] = data['뉴스제목'].apply(lambda x:remove_tag(x))
    port_list = []
    for i in range(data.shape[0]):
        category = data.iloc[i,0]
        company_name  = data.iloc[i,1]
        news_title = data.iloc[i,2]
        media = data.iloc[i,3]
        date =  data.iloc[i,4].strftime('%Y-%m-%d')
        news_url = data.iloc[i,5]
        writer = User.objects.get(username='admin')
        port_obj = Portfolio(category=category, company_name=company_name, media=media, date=date,\
                                news_title=news_title, news_url=news_url, writer=writer)
        port_list.append(port_obj)
    Portfolio.objects.bulk_create(port_list)
    print('포트폴리오 업로드')

def nan_remove(data):
    ret = str(data)
    str1 = 'https://help.naver.com/support/'
    if ret =='nan':
        ret = None
    elif str1 in ret:
        ret = None
    else:
        ret = ret
    return ret

def prof_send():
    data = pd.read_excel('./data/professor.xlsx')
    data.sort_values(by=['날짜'], inplace=True)
    data['뉴스URL'] = data['뉴스제목'].apply(lambda x:get_url(x))
    data['뉴스제목'] = data['뉴스제목'].apply(lambda x:remove_tag(x))
    data['기술소분류1'] = data['기술소분류1'].apply(lambda x:nan_remove(x))
    data['기술소분류2'] = data['기술소분류2'].apply(lambda x:nan_remove(x))
    prof_list = []
    for i in range(data.shape[0]):
        media = data.iloc[i,0]
        news_title = data.iloc[i,1]
        date = data.iloc[i,2]
        small_class_1 = data.iloc[i,3]
        small_class_2 = data.iloc[i,4]
        news_url = data.iloc[i,5]
        writer = User.objects.get(username='admin')
        prof_obj = Professor(media=media, date=date, small_class_1=small_class_1, small_class_2=small_class_2,\
                            news_title=news_title, news_url=news_url, writer=writer)
        prof_list.append(prof_obj)
    Professor.objects.bulk_create(prof_list)
    print('교수개발 업로드')
data = pd.read_excel('./data/rescue_all.xlsx')
data.head(2)
data.sort_values(by=['date'], inplace=True)
data['date'] = data['date'].apply(lambda x:str(x).replace('.','-'))

def resuce_send():
    data = pd.read_excel('./data/rescue_all.xlsx')
    data.sort_values(by=['date'], inplace=True)
    data['date'] = data['date'].apply(lambda x:str(x).replace('.','-'))
    rescue_list = []
    for i in range(data.shape[0]):
        date = data.iloc[i,4]
        area = data.iloc[i,0]
        case_num = data.iloc[i,1]
        company_name = data.iloc[i,2]
        court = data.iloc[i,3]
        subject = data.iloc[i,5]
        category = data.iloc[i,6]
        contents = data.iloc[i,10]
        news_title = data.iloc[i,12]
        news_url = data.iloc[i,11]
        writer = User.objects.get(username='admin')
        rescue_obj = Rescue(date=date, area=area, case_num=case_num, company_name=company_name, \
                            court=court, subject=subject, category=category, contents=contents,\
                            news_title=news_title, news_url=news_url, writer=writer)
        rescue_list.append(rescue_obj)
    Rescue.objects.bulk_create(rescue_list)
    print('회생법인 업로드')


if __name__ == "__main__":
    dart_send()
    invest_news_send()
    LP_company_send()
    main_company_send()
    protfolio_send()
    prof_send()
    resuce_send()
