from celery import shared_task
from news.task_module.professor import ProfessorNews
from news.task_module.news_crawler import NaverNewsCrawler
from news.models import (InvestNews,
                        LPCompany,
                        MainCompany,
                        Portfolio,
                        Professor
                        )

prof = ProfessorNews()
Naver = NaverNewsCrawler()


def data_send(self):
professor_last = prof.professor_prediction()
invest = Naver.naver_crawler_exe(mode='invest')
company = Naver.naver_crawler_exe(mode='company')
    print("back up data save")
    professor_last.to_csv(self.path2 + "/backup_data/" + datetime.today().strftime("%Y%m%d")+ "_Professor_Development_naver.csv",  encoding = "utf-8-sig", header=True, index=False) 
    company.to_csv(self.path2 + "/backup_data/" + datetime.today().strftime("%Y%m%d")+ "_company_naver.csv",  encoding = "utf-8-sig", header=True, index=False) 
    invest.to_csv(self.path2 + "/backup_data/" + datetime.today().strftime("%Y%m%d")+ "_Investment_attraction_naver.csv",  encoding = "utf-8-sig", header=True, index=False)
    return professor_last, port, lp, main, invest
