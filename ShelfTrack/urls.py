"""
URL configuration for ShelfTrack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Inventory.views import product_list, product_detail, low_stock_products
from Inventory.views import product_page, home, category_list, supplier_list
from Inventory.views import category_counts, supplier_counts

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', product_list),
    path('products/low-stock/', low_stock_products),
    path('products/<int:id>/', product_detail),
    path('product-page/', product_page),
    path('', home),
    path('categories/<int:id>/', category_list),
    path('suppliers/<int:id>/', supplier_list),
    path('category-counts/', category_counts),
    path('supplier-counts/', supplier_counts),
]
