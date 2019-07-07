from django.contrib import admin
from .models import (InvestNews,
                    LPCompany,
                    MainCompany,
                    Portfolio,
                    Professor,)
# Register your models here.
class InvestNewsAdmin(admin.ModelAdmin):
    list_display = ('date', 'news_title')


class LPCompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'news_title')


class MainCompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'news_title')


class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('news_title', 'small_class_1')


class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'news_title')


admin.site.register(InvestNews, InvestNewsAdmin)
admin.site.register(LPCompany, LPCompanyAdmin)
admin.site.register(MainCompany, MainCompanyAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
