from django.contrib import admin
from .models import Dart, Rescue
# Register your models here.
class DartAdmin(admin.ModelAdmin):
    list_display = ('date', 'company_name')


class RescueAdmin(admin.ModelAdmin):
    list_display = ('case_num', 'subject')

admin.site.register(Dart, DartAdmin)
admin.site.register(Rescue, RescueAdmin)
