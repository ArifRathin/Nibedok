from django.contrib import admin
from .models import *
# Register your models here.
class NotifTypeAdmin(admin.ModelAdmin):
    list_display = ['name','created_at','updated_at']
admin.site.register(NotificationType, NotifTypeAdmin)