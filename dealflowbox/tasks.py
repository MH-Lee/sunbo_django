from __future__ import absolute_import
from celery import shared_task
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from .models import DealFlowBox, UpdateChecker
from datetime import datetime
import time
import requests
import gspread, json
import pandas as pd


def update_data():
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    json_key='./utils/investanalytics-79366f3c1873.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_key, scope)
    url = 'https://docs.google.com/spreadsheets/d/14azI7dieHLWipvyy5-JO2kf2xl_skpUKhq6So0uIkgU/edit?usp=drive_web&ouid=100610050510801476562'
    gc = gspread.authorize(credentials).open_by_url(url)
    wks = gc.get_worksheet(0)
    dfb_df = pd.DataFrame(wks.get_all_records())
    dfb_df['date'] = dfb_df['작성 일자 Date'].apply(lambda x: datetime(*tuple(map(int, x.replace(' ','').split('.')))))
    dfb_df.columns
    dfb_df.sort_values('date', ascending=True, inplace=True)
    dfb_df2 = dfb_df[['date','기업명 Name of Company', '담당자 Person in Charge', \
                      '회사 업종 Sector','담당 오피스 Office','투자 단계 Funding Stage',\
                      '비즈니스 아이템 상세 Business Details','[Form Publisher] PDF URL']]
    dfb_df2.columns = ['Date', 'Company_name', 'Person_in_charge',\
                       'Sector', 'Office', 'Funding_stage',\
                       'Business Details','PDF_URL']
    last_update = UpdateChecker.objects.first()
    if last_update == None:
        dfb_list = list()
        for i in range(dfb_df2.shape[0]):
            print(i)
            date = dfb_df2.iloc[i,0].strftime('%Y-%m-%d')
            company_name = dfb_df2.iloc[i,1]
            person_in_charge = dfb_df2.iloc[i,2]
            sector = dfb_df2.iloc[i,3]
            office = dfb_df2.iloc[i,4]
            funding_stage = dfb_df2.iloc[i,5]
            business_detail = dfb_df2.iloc[i,6]
            PDF_URL = dfb_df2.iloc[i,7]
            dfb_obj = DealFlowBox(date=date, company_name=company_name, \
                                  file_url=PDF_URL, sector=sector, office=office,
                                  person_in_charge=person_in_charge,
                                  funding_stage=funding_stage,
                                  business_detail=business_detail)
            dfb_list.append(dfb_obj)
        # UpdateChecker.objects.all().delete()
        uc_obj = UpdateChecker(recent_date=dfb_df2.iloc[i,0].strftime('%Y-%m-%d'),\
                               status=1)
        uc_obj.save()
        DealFlowBox.objects.bulk_create(dfb_list)
        print("upload complete")
    else:
        last_update = pd.to_datetime(last_update.recent_date)
        # last_update = pd.Timestamp('2019-06-02 00:00:00')
        if last_update >= dfb_df2.tail(1)['Date'].values[0]:
            print("최신데이터")
            pass
        else:
            dfb_df_new = dfb_df2[dfb_df2['Date'] > last_update]
            dfb_df_new
            i =1
            dfb_list_new = list()
            for i in range(dfb_list.shape[0]):
                print(i)
                date = dfb_df_new.iloc[i,0].strftime('%Y-%m-%d')
                company_name = dfb_df_new.iloc[i,1]
                person_in_charge = dfb_df_new.iloc[i,2]
                sector = dfb_df_new.iloc[i,3]
                office = dfb_df_new.iloc[i,4]
                funding_stage = dfb_df_new.iloc[i,5]
                business_detail = dfb_df_new.iloc[i,6]
                PDF_URL = dfb_df_new.iloc[i,7]
                dfb_obj = DealFlowBox(date=date, company_name=company_name, \
                                      file_url=PDF_URL, sector=sector, office=office,
                                      person_in_charge=person_in_charge,
                                      funding_stage=funding_stage)
            dfb_list_new.append(dfb_obj)
            # UpdateChecker.objects.all().delete()
            uc_obj_new = UpdateChecker(recent_date=dfb_df_new.iloc[i,0].strftime('%Y-%m-%d'),\
                                   status=1)
            uc_obj_new.save()
            DealFlowBox.objects.bulk_create(dfb_list_new)
            print("upload complete")

@shared_task
def dealflowbox_update():
    update_data()
    return True