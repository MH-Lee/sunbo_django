from django.db import models
from django.conf import settings
# Create your models here.
#투자 뉴스
class InvestNews(models.Model):
    media = models.CharField(max_length=20, verbose_name="신문사")
    date = models.CharField(max_length=10, verbose_name="날짜")
    news_title = models.CharField(max_length=200, verbose_name="뉴스제목")
    news_url = models.CharField(max_length=300, verbose_name="뉴스URL")
    company_name = models.CharField(max_length=100, verbose_name="기업명", null=True, blank=True)
    company_address = models.CharField(max_length=128, verbose_name="기업주소", null=True, blank=True)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                verbose_name='작성자')
    registered_dttm = models.DateTimeField(auto_now_add=True,
                                            verbose_name='등록시간')

    def __str__(self):
        return self.media

    class Meta:
        db_table = 'invest_news'
        verbose_name = '투자뉴스'
        verbose_name_plural = '투자뉴스'


#LP기업
class LPCompany(models.Model):
    category = models.CharField(max_length=20, verbose_name="카테고리")
    date = models.CharField(max_length=10, verbose_name="날짜")
    company_name = models.CharField(max_length=20, verbose_name="기업명")
    news_title = models.CharField(max_length=200, verbose_name="뉴스제목")
    news_url = models.CharField(max_length=300, verbose_name="뉴스URL")
    media = models.CharField(max_length=20, verbose_name="신문사")
    writer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                verbose_name='작성자')
    registered_dttm = models.DateTimeField(auto_now_add=True,
                                            verbose_name='등록시간')

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = 'LP_company'
        verbose_name = 'LP기업'
        verbose_name_plural = 'LP기업'

# 관계사
class MainCompany(models.Model):
    category = models.CharField(max_length=20, verbose_name="카테고리")
    date = models.CharField(max_length=10, verbose_name="날짜")
    company_name = models.CharField(max_length=128, verbose_name="기업명")
    news_title = models.CharField(max_length=300, verbose_name="뉴스제목")
    news_url = models.CharField(max_length=300, verbose_name="뉴스URL")
    media = models.CharField(max_length=20, verbose_name="신문사")
    writer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                verbose_name='작성자')
    registered_dttm = models.DateTimeField(auto_now_add=True,
                                            verbose_name='등록시간')

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = 'main_company'
        verbose_name = '자매기업'
        verbose_name_plural = '자매기업'


#교수개발 뉴스
class Professor(models.Model):
    date = models.CharField(max_length=10, verbose_name="날짜")
    media = models.CharField(max_length=20, verbose_name="신문사")
    news_title = models.CharField(max_length=200, verbose_name="관련뉴스")
    news_url = models.CharField(max_length=300, verbose_name="뉴스URL")
    small_class_1 = models.CharField(max_length=100, verbose_name="기술소분류1", null=True)
    small_class_2 = models.CharField(max_length=100, verbose_name="기술소분류2",null=True)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                verbose_name='작성자')
    registered_dttm = models.DateTimeField(auto_now_add=True,
                                            verbose_name='등록시간')

    def __str__(self):
        return self.news_title

    class Meta:
        db_table = 'professor'
        verbose_name = '교수개발 뉴스'
        verbose_name_plural = '교수개발 뉴스'

#LP기업
class Portfolio(models.Model):
    category = models.CharField(max_length=10, verbose_name="카테고리")
    date = models.CharField(max_length=10, verbose_name="날짜")
    company_name = models.CharField(max_length=128, verbose_name="기업명")
    media = models.CharField(max_length=20, verbose_name="신문사")
    news_title = models.CharField(max_length=200, verbose_name="뉴스제목")
    news_url = models.CharField(max_length=300, verbose_name="뉴스URL")
    writer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                verbose_name='작성자')
    registered_dttm = models.DateTimeField(auto_now_add=True,
                                            verbose_name='등록시간')

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = 'portfolio'
        verbose_name = '포트폴리오'
        verbose_name_plural = '포트폴리오'
