from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from .models import Rescue

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
    all_rescue = Rescue.objects.all().order_by('-id')
    page = int(request.GET.get('p',1))
    paginator = Paginator(all_rescue, 20)
    rescues = paginator.get_page(page)
    return render(request, 'information/rescue_list.html', {'rescues':rescues})