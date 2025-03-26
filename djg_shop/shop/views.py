from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count, Avg, Max, Min, Sum
from django.db.models import Value, F, Func
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer

@api_view()
def all_products(request):
    
    # get data
    query_set = Product.objects.all()
    
    # create serializer for the data
    serializer = ProductSerializer(query_set, many=True) # pass many=True so the serializer knows to iterate
    
    data = serializer.data
    
    return Response(data)


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