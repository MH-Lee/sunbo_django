from rest_framework import serializers
from information.models import Dart, Rescue


class DartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dart
        fields = '__all__'

class RescueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rescue
        fields = ('id',
                  'date',
                  'area',
                  'case_num',
                  'company_name',
                  'company_address',
                  'ceo',
                  'court',
                  'subject',
                  'news_title',
                  'news_url')