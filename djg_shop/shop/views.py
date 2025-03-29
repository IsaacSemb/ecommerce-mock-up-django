from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count, Avg, Max, Min, Sum
from django.db.models import Value, F, Func
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Category, Product
from .serializers import ProductSerializer, CategorySerializer

@api_view(['GET','POST'])
def all_products(request):
    
    if request.method == 'GET':
        query_set = Product.objects.select_related('category').all()[:5]
        serializer = ProductSerializer(
            query_set, 
            many=True, 
            context={'request':request}
            ) 
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('ok')



notes = """

retrieve the object and pass it to the serializer


"""

@api_view()
def product_detail(request,id):
    
    # get the product you want to get 
    product = get_object_or_404(Product, pk=id)
    
    # srialisze it using the responsible serializer
    serializer = ProductSerializer(product)

    # get the data from it and pass it and pass it as a response
    data = serializer.data
    
    return Response(data)

@api_view()
def category_detail(request, pk): 
    return Response('ok')
    category = get_object_or_404(Category, pk=id)
    serializer = CategorySerializer(category)
    data = serializer.data
    
    return Response(data)

