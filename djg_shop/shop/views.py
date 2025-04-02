from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count, Avg, Max, Min, Sum
from django.db.models import Value, F, Func
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
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


class AllProducts(APIView):
    def get(self, request):
        print("\n## here ##\n")
        # logic from the get if statement
        query_set = Product.objects.select_related('category').all()[:5]
        serializer = ProductSerializer(
            query_set, 
            many=True, 
            context={'request':request}
            ) 
        return Response(serializer.data)
        
    
    def post(self, request):
        # logic from the post if statement
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('ok')
    


notes = """

retrieve the object and pass it to the serializer


"""

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request,id):
    # get the product you want to work with 
    product = get_object_or_404(Product, pk=id)
        
    if request.method == 'GET':
        # serialisze it using the responsible serializer
        serializer = ProductSerializer(product)
        # get the data from it and pass it and pass it as a response
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)
    
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data = request.data, )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        
        # check if it has order items associated with it
        if product.orderitems.count()>0:
            return Response(data={'error':'Product cant be deleted because it is associated to an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
@api_view(['GET','POST'])
def category(request):
    
    if request.method == 'GET':
        
        query_set = ( Category.objects
        .annotate( product_count = Count('product_category'))
        .all()
        )
        
        serializer = CategorySerializer(
            query_set, 
            many=True, 
            context={'request':request}
            ) 
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = CategorySerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk): 
    
    category = get_object_or_404(Category, pk=pk)
    

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        data = serializer.data    
        return Response(data)

    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    elif request.method == 'DELETE':        
        if category.product_category.count() > 0:
            return Response(data={'error': "Category has products associated with it"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    
