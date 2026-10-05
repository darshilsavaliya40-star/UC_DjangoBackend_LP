from django.contrib import admin
from .models import Product
from .models import Category
from .models import Supplier

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ['created_by']
    
admin.site.register(Category)
admin.site.register(Supplier)