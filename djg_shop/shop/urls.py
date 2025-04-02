from django.urls import path
from . import views

urlpatterns = [
    # path('products/', views.all_products), # function view
    path('products/', views.AllProducts.as_view()), # class view
    path('products/<int:id>/', views.product_detail),
    path('category/', views.category),
    path('category/<int:pk>/', views.category_detail, name='category-detail')
]
