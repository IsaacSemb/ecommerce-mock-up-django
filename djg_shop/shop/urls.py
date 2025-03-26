from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.all_products),
    path('products/<id>', views.product_detail)
]
