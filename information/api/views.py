from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from information.models import Rescue, Dart

from information.api.serializers import (
    DartSerializer,
    RescueSerializer
)
from utils.paginations import StandardResultPagination

class DateAPIView(generics.ListAPIView):
    queryset = Dart.objects.all().order_by('-date')
    serializer_class = DartSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = Dart.objects.all()
        date_by = self.request.GET.get('date')
        ticker_by = self.request.GET.get('ticker')
        name_by = self.request.GET.get('company_name')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if ticker_by:
            queryset = queryset.filter(ticker=ticker_by)
        if name_by:
            queryset = queryset.filter(company_name=name_by)
        return queryset

class RescueAPIView(generics.ListAPIView):
    queryset = Rescue.objects.all().order_by('-date')
    serializer_class = RescueSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = Rescue.objects.all()
        date_by = self.request.GET.get('date')
        case_num_by = self.request.GET.get('case_num')
        name_by = self.request.GET.get('company_name')
        area_by = self.request.GET.get('area')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if case_num_by:
            queryset = queryset.filter(case_num=case_num_by)
        if name_by:
            queryset = queryset.filter(company_name=name_by)
        if area_by:
            queryset = queryset.filter(area=area_by)
        return queryset