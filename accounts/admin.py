from django.contrib import admin
from .models import OnspaceUser
# Register your models here.

class OnspaceAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')

admin.site.register(OnspaceUser, OnspaceAdmin)