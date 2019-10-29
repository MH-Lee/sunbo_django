from .models import DealFlowBox, UpdateChecker
from django.shortcuts import render, redirect
# from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.

# dart_view
def dfb_list(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.method == 'GET':
        query =  request.GET.get('q')
        order_by = request.GET.get('order_by')
        direction = request.GET.get('direction')
        if order_by != None:
            if direction == 'asc':
                dfbs = DealFlowBox.objects.all().order_by(order_by)
            else:
                dfbs = DealFlowBox.objects.all().order_by('-{}'.format(order_by))
        else:
            try:
                dfbs = DealFlowBox.objects.filter(
                    Q(company_name__icontains=query) |\
                    Q(sector__icontains=query) |\
                    Q(person_in_charge__icontains=query)|\
                    Q(office__icontains=query)
                ).order_by('-id')
                direction = None
            except:
                dfbs = DealFlowBox.objects.all().order_by('-id')
                direction = None
    else:
        dfbs = DealFlowBox.objects.all().order_by('-id')
        direction = None
    page = int(request.GET.get('p',1))
    try:
        paginator = Paginator(dfbs, 15)
        dfb_infos = paginator.get_page(page)
    except:
        paginator = Paginator(dfbs, 15)
        dfb_infos = None
    return render(request, 'dealflowbox/deal_list.html', {'dfb_infos':dfb_infos, 'order_by':order_by, 'direction':direction})
