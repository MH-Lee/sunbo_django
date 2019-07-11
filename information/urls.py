    
from django.urls import path, include
from . import views

urlpatterns = [
    path('rescue_list/', views.rescue_list, name='rescue_list'),
    path('dart_list/', views.dart_list, name='dart_list'),
    path('rescue_detail/<int:pk>', views.rescue_detail, name='rescue_detail'),
]