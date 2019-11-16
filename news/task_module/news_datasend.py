import ast
import multiprocessing
import pickle
import pandas as pd
import numpy as np
import joblib
import re
import os
from collections import namedtuple
from sklearn.model_selection import train_test_split
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import konlpy
from konlpy.tag import Kkma, Okt, Hannanum, Twitter
from datetime import datetime
#tokenize & word2vec packages
from soynlp import DoublespaceLineCorpus
from soynlp.word import WordExtractor
from soynlp.tokenizer import LTokenizer
from soynlp.noun import NewsNounExtractor
from gensim.models import Word2Vec
import gensim, logging
from gensim.test.utils import common_texts, get_tmpfile
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.summarization import keywords
from newspaper import Article
from newspaper import fulltext
from news.task_module.news_crawler import NaverNewsCrawler
from news.models import (LPCompany, 
                         MainCompany, 
                         InvestNews,
                         Professor,
                         Portfolio)
from accounts.models import User

class DataProcessingSend:
    def __init__(self):
        self.path = '/home/ubuntu/sunbo_django/recommender/models/'
        self.path2 = '/home/ubuntu/sunbo_django/news/task_module'
        self.ko_stopwords = pd.read_csv(self.path2 + '/nlp_material/korean_stopwords.txt')
        self.token_stops = pd.read_csv(self.path2 + '/nlp_material/token_stopwords.csv', engine='python', encoding='cp949')['stopwords'].tolist()
        self.doc_vectorizer = Doc2Vec.load(self.path + 'Doc2vec1.model')
        self.doc_set = pd.read_excel(self.path2 + '/nlp_material/doc_set.xlsx')
        self.doc_set['token'] = self.doc_set['token'].apply(lambda x: x.replace("['","").replace("']","").split("', '"))
        # self.new_small = pd.read_excel('./nlp_material/new_small_class.xlsx')
        self.mlp_clf = joblib.load(self.path2 + '/nlp_material/mlp_clf.sav')
        self.mlp_clf2 = joblib.load(self.path2 + '/nlp_material/mlp_clf2.sav')
        self.Naver = NaverNewsCrawler()
        if os.path.exists(self.path2+ '/backup_data/') == False:
            os.mkdir(self.path2 + '/backup_data/')
        print("datasend start!")


    def noun_corpus(self, sents):
        noun_extractor = NewsNounExtractor()
        nouns = noun_extractor.train_extract(sents)
        from soynlp.tokenizer import NounLMatchTokenizer
        noun_scores = {noun:score[0] for noun, score in nouns.items() if len(noun) > 1}
        tokenizer = NounLMatchTokenizer(noun_scores)
        corpus = [tokenizer.tokenize(sent) for sent in sents]
        return corpus

    def stopwords_remove(self, stops,corpus):
        docs=[]
        for i in range(len(corpus)):
            words=[]
            for w in corpus[i]:
                if (not w in stops) & (len(w)>1):
                    words.append(w)
            docs.append(words)
        return docs

    def make_professor_token(self, doc_df):
        worrd_list = []
        # 텍스트를 가지고 있는 리스트
        for i in list(doc_df['content']):
            # 숫자 및 특수문자 제거.
            t = re.sub('[\d\s0-9]',' ',str(i)).strip()
            t = re.sub('[=+,#/\?:^$.@*\"※~&%ㆍ·⌬◎◳▢▪!』․\\‘|\(\)\[\]\<\>`\'…》→’“”;●•]', ' ', t)
            t = re.sub('\xad', ' ', t)
            t = re.sub('\n', ' ', t)
            t = re.sub('  ', ' ', t)
            t = re.sub('  ', ' ', t)
            t = re.sub('  ', ' ', t)
            t = re.sub('및', '', t)
            worrd_list.append(t)
        df_corpus = self.noun_corpus(worrd_list)
        #stopwords 제거
        stops = self.ko_stopwords
        docs=[]
        for i in range(len(df_corpus)):
            words=[]
            for w in df_corpus[i]:
                if (not w in stops) & (len(w)>1):
                    words.append(w)
            docs.append(words)
        return docs

    def make_professor_content(self):
        professor = self.Naver.naver_crawler_exe(mode='professor')
        ko_stopwords=list(self.ko_stopwords['stopwords'])
        text=[]
        keyword=[]
        for i in range(len(professor)):
            url = professor['link'][i]
            a = Article(url, language='ko')
            a.download()
            a.parse()
            text.append(a.text)
        professor['content'] = text
        professor['token'] = self.make_professor_token(professor)
        return professor

    def professor_news_zifslow(self):
        professor = self.make_professor_content()
        tokens = [ t for d in professor['token'] for t in d]
        text = nltk.Text(tokens, name='NMSC')
        fdist = text.vocab()
        df_fdist = pd.DataFrame.from_dict(fdist, orient='index')
        df_fdist.columns = ['frequency']
        df_fdist['term'] = list(df_fdist.index)
        df_fdist = df_fdist.reset_index(drop=True)
        df_fdist = df_fdist.sort_values(["frequency"], ascending=[False])
        df_fdist = df_fdist.reset_index(drop=True)
        df_fdist.head(100)
        zif_list = pd.DataFrame(df_fdist[(df_fdist['frequency'] <= 2)]['term'])
        zif_list.columns = ['stopwords']
        zif_list = zif_list.reset_index(drop=True)
        zif_stops = list(zif_list['stopwords'])
        print(zif_stops)
        docs = self.stopwords_remove(zif_stops, professor['token'])
        docs = self.stopwords_remove(self.token_stops, docs)
        professor['token'] = docs
        professor['lable'] = ['']*len(professor)
        tagged_professor_docs = [TaggedDocument(d, c) for d, c in professor[['token', 'lable']].values]

        category_dic = {}
        big = list(set(self.doc_set['new_class']))
        for i in range(len(big)):
            temp = big[i]
            s_temp = list (set(self.doc_set[self.doc_set['new_class']==temp].new_small_class))
            category_dic[temp]=s_temp
        return category_dic, tagged_professor_docs, docs, professor

    def professor_prediction(self):
        category_dic, tagged_professor_docs, docs, professor = self.professor_news_zifslow()
        X_professor = [self.doc_vectorizer.infer_vector(doc.words) for doc in tagged_professor_docs]
        # y_professor = [doc.tags for doc in tagged_professor_docs]
        y_professor_pred = self.mlp_clf.predict(X_professor)
        y_professor_prob = self.mlp_clf.predict_proba(X_professor)
        L = np.argsort(-y_professor_prob, axis=1)
        two_pred = L[:,0:3]
        class_dic = {self.mlp_clf.classes_[i]: i for i in range(len(self.mlp_clf.classes_))}
        key_list = list(class_dic.keys())
        val_list = list(class_dic.values())

        dd = []
        for i in range(len(y_professor_prob)):
            first = two_pred[i][0]
            second = two_pred[i][1]
            thrid = two_pred[i][2]
            label = list([key_list[val_list.index(first)],key_list[val_list.index(second)],key_list[val_list.index(thrid)]])
            dd.append({'title':professor['title'][i],
                       'predicted_label1':label[0], 'predicted_label2': label[1], 'predicted_label3': label[2]})

        y_professor_pred = self.mlp_clf2.predict(X_professor)
        y_professor_pred = self.mlp_clf2.predict_proba(X_professor)
        L = np.argsort(-y_professor_pred, axis=1)
        two_pred = L[:,0:3]
        class_dic = {self.mlp_clf2.classes_[i]: i for i in range(len(self.mlp_clf2.classes_))}
        key_list = list(class_dic.keys())
        val_list = list(class_dic.values())

        second_result = []
        for i in range(len(X_professor)):
            tt = category_dic[dd[i]['predicted_label1']] + category_dic[dd[i]['predicted_label2']]
            tt = [x for x in tt if x in key_list]
            ttt = list({ your_key: class_dic[your_key] for your_key in tt }.values())
            tttt = [x for x in L[i] if x in ttt]
            first = tttt[0]
            second = tttt[1]
            third = tttt[2]
            label = list([key_list[val_list.index(first)],key_list[val_list.index(second)],key_list[val_list.index(third)]])
            second_result.append({'date':professor['date'][i],'title':professor['title'][i],
                                   'predicted_label1':label[0], 'predicted_label2': label[1],
                                 'link':professor['link'][i],'press':professor['press'][i]})

        professor_result = pd.DataFrame(second_result,columns=['date','title','predicted_label1','predicted_label2','link','press'])
        return professor_result

    def prof_send(self, data):
        prof_list = []
        for i in range(data.shape[0]):
            media = data.loc[i, 'press']
            news_title = data.iloc[i, 'title']
            date = data.iloc[i,2].strftime('%Y-%m-%d')
            small_class_1 = data.iloc[i,'predicted_label1']
            small_class_2 = data.iloc[i,'predicted_label2']
            news_url = data.iloc[i,'link']
            writer = User.objects.get(username='admin')
            prof_obj = Professor(media=media, date=date, small_class_1=small_class_1, small_class_2=small_class_2,\
                                news_title=news_title, news_url=news_url, writer=writer)
            prof_list.append(prof_obj)
        Professor.objects.bulk_create(prof_list)
        print('교수개발 업로드')

    def invest_news_send(self, data):
        invest_list = []
        for i in range(data.shape[0]):
            media = data.loc[i,0]
            date =  data.loc[i,2].strftime('%Y-%m-%d')
            news_title = data.loc[i,1]
            news_url = data.loc[i,3]
            writer = User.objects.get(username='admin')
            invest_obj = InvestNews(media=media, date=date, news_title=news_title,\
                                    news_url=news_url, writer=writer)
            invest_list.append(invest_obj)
        InvestNews.objects.bulk_create(invest_list)
        print('invest_news 업로드')

    def LP_company_send(self, data):
        lpc_list = []
        for i in range(data.shape[0]):
            category = data.iloc[i,0]
            company_name  = data.iloc[i,1]
            news_title = data.iloc[i,2]
            media = data.iloc[i,3]
            date =  data.iloc[i,4].strftime('%Y-%m-%d')
            print(date)
            news_url = data.iloc[i,5]
            writer = User.objects.get(username='admin')
            lpc_obj = LPCompany(category=category, company_name=company_name, media=media, date=date,\
                                    news_title=news_title, news_url=news_url, writer=writer)
            lpc_list.append(lpc_obj)
        LPCompany.objects.bulk_create(lpc_list)
        print('LP기업 업로드')

    def main_company_send(self, data):
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

    def portfolio_send(self, data):
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

    def data_send(self):
        professor_last = self.professor_prediction()
        invest = self.Naver.naver_crawler_exe(mode='invest')
        company = self.Naver.naver_crawler_exe(mode='company')
        port = company[company['category'] == '포트폴리오'].reset_index(drop=True)
        lp = company[company['category'] == 'LP기업'].reset_index(drop=True)
        main = company[company['category'] == '자매기업'].reset_index(drop=True)
        print("back up data save")
        professor_last.to_csv(self.path2 + "/backup_data/" + datetime.today().strftime("%Y%m%d")+ "_Professor_Development_naver.csv",  encoding = "utf-8-sig", header=True, index=False) 
        company.to_csv(self.path2 + "/backup_data/" + datetime.today().strftime("%Y%m%d")+ "_company_naver.csv",  encoding = "utf-8-sig", header=True, index=False) 
        invest.to_csv(self.path2 + "/backup_data/" + datetime.today().strftime("%Y%m%d")+ "_Investment_attraction_naver.csv",  encoding = "utf-8-sig", header=True, index=False)
        print("DB send start")
        return professor_last, port, lp, main, invest
        # LPCompany
        # MainCompany 
        # InvestNews
        # Professor
        # Portfolio
        # print("DB save")

# dps = DataProcessingSend()
# professor_last, port, lp, main, invest = dps.data_send()
