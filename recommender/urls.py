from django.urls import path
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path('introduction/', views.introduction, name='service_intro'),
    path('network/', views.network, name='network'),
    path('startup/', TemplateView.as_view(template_name="./project/st_net2.html"), name='startup'),
]
