from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import (LPCompany, 
                    MainCompany, 
                    InvestNews,
                    Professor,
                    Portfolio,                    
                    )

# Create your views here.
# main_company_view
def LP_company_list(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.method == 'GET':
        query =  request.GET.get('q')
        try:
            lp_company_obj = LPCompany.objects.filter(
                Q(media__icontains=query) | Q(news_title__icontains=query) |\
                Q(company_name__icontains=query) | Q(category__icontains=query)
            ).order_by('-id')
        except:
            lp_company_obj = LPCompany.objects.all().order_by('-id')    
    else:
        lp_company_obj = LPCompany.objects.all().order_by('-id')
    page = int(request.GET.get('p',1))
    try:
        paginator = Paginator(lp_company_obj, 15)
        lp_company_info = paginator.get_page(page)
    except:
        paginator = Paginator(lp_company_obj, 15)
        lp_company_info = NULL
    return render(request, 'news/lp_company_list.html', {'lp_company_info':lp_company_info})

# main_company_view
def main_company_list(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.method == 'GET':
        query =  request.GET.get('q')
        try:
            main_company_obj = MainCompany.objects.filter(
               Q(media__icontains=query) | Q(news_title__icontains=query) |\
                Q(company_name__icontains=query) | Q(category__icontains=query)
            ).order_by('-id')
        except:
            main_company_obj = MainCompany.objects.all().order_by('-id')    
    else:
        main_company_obj = MainCompany.objects.all().order_by('-id')
    page = int(request.GET.get('p',1))
    try:
        paginator = Paginator(main_company_obj, 15)
        main_company_info = paginator.get_page(page)
    except:
        paginator = Paginator(main_company_obj, 15)
        main_company_info = NULL
    return render(request, 'news/main_company_list.html', {'main_company_info':main_company_info})

# portfolio_view
def portfolio_list(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.method == 'GET':
        query =  request.GET.get('q')
        try:
            _port_obj = Portfolio.objects.filter(
               Q(media__icontains=query) | Q(news_title__icontains=query) |\
                Q(company_name__icontains=query) | Q(category__icontains=query)
            ).order_by('-id')
        except:
            _port_obj = Portfolio.objects.all().order_by('-id')    
    else:
        _port_obj = Portfolio.objects.all().order_by('-id')
    page = int(request.GET.get('p',1))
    try:
        paginator = Paginator(_port_obj, 15)
        portfolio_info = paginator.get_page(page)
    except:
        paginator = Paginator(_port_obj, 15)
        portfolio_info = NULL
    return render(request, 'news/portfolio_list.html', {'portfolio_info':portfolio_info})

# investment_news_view
def investment_news_list(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.method == 'GET':
        query =  request.GET.get('q')
        try:
            _invest_obj = InvestNews.objects.filter(
               Q(media__icontains=query) | Q(news_title__icontains=query) |\
                Q(company_name__icontains=query) | Q(category__icontains=query)
            ).order_by('-id')
        except:
            _invest_obj = InvestNews.objects.all().order_by('-id')    
    else:
        _invest_obj = InvestNews.objects.all().order_by('-id')
    page = int(request.GET.get('p',1))
    try:
        paginator = Paginator(_invest_obj, 15)
        investment_info = paginator.get_page(page)
    except:
        paginator = Paginator(_invest_obj, 15)
        investment_info = NULL
    return render(request, 'news/investment_news_list.html', {'investment_info':investment_info})


# portfolio_view
def professor_list(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.method == 'GET':
        query =  request.GET.get('q')
        try:
            _professor_obj = Professor.objects.filter(
               Q(media__icontains=query) | Q(news_title__icontains=query) |\
                Q(small_class_2__icontains=query) | Q(small_class_2__icontains=query)
            ).order_by('-id')
        except:
            _professor_obj = Professor.objects.all().order_by('-id')    
    else:
        _professor_obj = Professor.objects.all().order_by('-id')
    page = int(request.GET.get('p',1))
    try:
        paginator = Paginator(_professor_obj, 15)
        professor_info = paginator.get_page(page)
    except:
        paginator = Paginator(_professor_obj, 15)
        professor_info = NULL
    return render(request, 'news/professor_list.html', {'professor_info':professor_info})

