from django.contrib import admin
from .models import *
# Register your models here.
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
admin.site.register(ProductCategory,ProductCategoryAdmin)