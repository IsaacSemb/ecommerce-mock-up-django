from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.all_products),
    path('products/<int:id>/', views.product_detail),
    path('category/', views.category),
    path('category/<int:pk>/', views.category_detail, name='category-detail')
]
