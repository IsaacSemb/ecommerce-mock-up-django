# django imports
from django.urls import include, path

# rest framework
# from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers

# local
from . import views
from pprint import pprint

# router = SimpleRouter()
# router = DefaultRouter() # overwrite the simple router
router = routers.DefaultRouter() # overwrite the default router with the nested one

router.register('products',views.ProductViewSet, basename='products')
router.register('category',views.CategoryViewSet)

products_router = routers.NestedDefaultRouter(
    parent_router=router, 
    parent_prefix='products',
    lookup='product'
    )

products_router.register(
    prefix='reviews',
    viewset=views.ReviewViewSet,
    basename='products-reviews'
    )

# carts
router.register('carts',views.CartViewSet)

# created a nested router to do cart items
cart_router = routers.NestedDefaultRouter(
    parent_router=router, 
    parent_prefix='carts',
    lookup='cart'
    )

cart_router.register(
    prefix='items',
    viewset=views.CartItemViewSet,
    basename='cart-items'
    )

# urlpatterns = [
#     # path('products/', views.all_products), # function view-----
#     path('products/', views.AllProducts.as_view()), # class view 
#     # path('products/<int:id>/', views.product_details),-----
#     path('products/<int:pk>/', views.ProductDetail.as_view()),
#     path('category/', views.CategoryList.as_view()),
#     # path('category/<int:pk>/', views.category_detail, name='category-detail')-----
#     path('category/<int:pk>/', views.CategoryDetail.as_view())
# ]

# urlpatterns = router.urls + products_router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
    path('', include(cart_router.urls))
]


