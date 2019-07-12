from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Rescue, Dart

# Create your views here.
def rescue_detail(request, pk):
    try:
        rescue = Rescue.objects.get(pk=pk)
    except Rescue.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다.')
    return render(request, 'information/rescue_detail.html', {'rescue':rescue})

def rescue_list(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.method == 'GET':
        query =  request.GET.get('q')
        try:
            rescue_obj = Rescue.objects.filter(
                Q(area__icontains=query) | Q(case_num__icontains=query) |\
                Q(subject__icontains=query) | Q(category__icontains=query) |\
                Q(news_title__icontains=query)
            ).order_by('-id')
        except:
            rescue_obj = Rescue.objects.all().order_by('-id')    
    else:
        rescue_obj = Rescue.objects.all().order_by('-id')
    page = int(request.GET.get('p',1))
    try:
        paginator = Paginator(rescue_obj, 15)
        rescues = paginator.get_page(page)
    except:
        paginator = Paginator(rescue_obj, 15)
        rescues = NULL
    return render(request, 'information/rescue_list.html', {'rescues':rescues})

# dart_view
def dart_list(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.method == 'GET':
        query =  request.GET.get('q')
        try:
            darts = Dart.objects.filter(
                Q(company_name__icontains=query) | Q(news_title__icontains=query) |  Q(another_name__icontains=query)
            ).order_by('-id')
        except:
            darts = Dart.objects.all().order_by('-id')    
    else:
        darts = Dart.objects.all().order_by('-id')
    page = int(request.GET.get('p',1))
    try:
        paginator = Paginator(darts, 15)
        dart_infos = paginator.get_page(page)
    except:
        paginator = Paginator(darts, 15)
        dart_infos = NULL
    return render(request, 'information/dart_list.html', {'dart_infos':dart_infos})