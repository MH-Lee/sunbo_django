from django.contrib import admin
from .models import OnsideUser
# Register your models here.

class OnsideAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')

admin.site.register(OnsideUser, OnsideAdmin)