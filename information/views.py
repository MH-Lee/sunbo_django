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
        order_by = request.GET.get('order_by')
        direction = request.GET.get('direction')
        if order_by != None:
            if direction == 'asc':
                rescue_obj = Rescue.objects.all().order_by(order_by)
            else:
                rescue_obj = Rescue.objects.all().order_by('-{}'.format(order_by))
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
    index = rescues.number -1 
    max_index = len(paginator.page_range) 
    start_index = index -2 if index >= 2 else 0 
    if index < 2 : 
        end_index = 5-start_index 
    else : 
        end_index = index+3 if index <= max_index - 3 else max_index 
    page_range = list(paginator.page_range[start_index:end_index]) 
    return render(request, 'information/rescue_list.html', {'rescues':rescues, 'order_by':order_by , 'direction':direction,\
                                                            'page_range':page_range, 'max_index':max_index-2})

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
            else:
                darts = Dart.objects.all().order_by('-{}'.format(order_by))
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
    return render(request, 'information/dart_list.html', {'dart_infos':dart_infos, 'order_by':order_by, 'direction':direction})