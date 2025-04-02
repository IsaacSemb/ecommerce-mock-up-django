# django imports
from django.urls import path

# rest framework
from rest_framework.routers import SimpleRouter

# local
from . import views

urlpatterns = [
    # path('products/', views.all_products), # function view
    path('products/', views.AllProducts.as_view()), # class view
    # path('products/<int:id>/', views.product_details),
    path('products/<int:pk>/', views.ProductDetail.as_view()),
    path('category/', views.CategoryList.as_view()),
    # path('category/<int:pk>/', views.category_detail, name='category-detail')
    path('category/<int:pk>/', views.CategoryDetail.as_view())
]
