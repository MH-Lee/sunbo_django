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

def add_one(a):
    a +=1
    return a

def rescue_list(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.method == 'GET':
        query =  request.GET.get('q')
        order_by = request.GET.get('order_by')
        direction = request.GET.get('direction')
        if order_by != None:
            if direction == 'asc':
                rescue_obj = Rescue.objects.all().order_by(order_by)
                direction = 'desc'
            else:
                rescue_obj = Rescue.objects.all().order_by('-{}'.format(order_by))
                direction = 'asc'
        else:   
            try:
                rescue_obj = Rescue.objects.filter(
                    Q(area__icontains=query) | Q(case_num__icontains=query) |\
                    Q(subject__icontains=query) | Q(company_name__icontains=query) |\
                    Q(category__icontains=query) | Q(news_title__icontains=query)
                ).order_by('-id')
                direction = None
            except:
                rescue_obj = Rescue.objects.all().order_by('-id')
                direction = None
    else:
        rescue_obj = Rescue.objects.all().order_by('-id')
        direction = None
    page = int(request.GET.get('p',1))
    try:
        paginator = Paginator(rescue_obj, 15)
        rescues = paginator.get_page(page)
    except:
        paginator = Paginator(rescue_obj, 15)
        rescues = NULL
    return render(request, 'information/rescue_list.html', {'rescues':rescues, 'direction':direction})

# dart_view
def dart_list(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.method == 'GET':
        query =  request.GET.get('q')
        order_by = request.GET.get('order_by')
        direction = request.GET.get('direction')
        if order_by != None:
            if direction == 'asc':
                darts = Dart.objects.all().order_by(order_by)
                direction = 'desc'
            else:
                darts = Dart.objects.all().order_by('-{}'.format(order_by))
                direction = 'asc'
        else:   
            try:
                darts = Dart.objects.filter(
                    Q(company_name__icontains=query) | Q(news_title__icontains=query) |  Q(another_name__icontains=query)
                ).order_by('-id')
                direction = None
            except:
                darts = Dart.objects.all().order_by('-id')
                direction = None
    else:
        darts = Dart.objects.all().order_by('-id')
        direction = None
    page = int(request.GET.get('p',1))
    try:
        paginator = Paginator(darts, 15)
        dart_infos = paginator.get_page(page)
    except:
        paginator = Paginator(darts, 15)
        dart_infos = NULL
    return render(request, 'information/dart_list.html', {'dart_infos':dart_infos, 'direction':direction})