from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count, Avg, Max, Min, Sum
from django.db.models import Value, F, Func

# restframework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.mixins import ListModelMixin, CreateModelMixin 
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView 

# personal imports
from .models import Category, Product
from .serializers import ProductSerializer, CategorySerializer

# DEPRACATED
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

# DEPRACATED
class AllProducts_OLD(APIView):
    def get(self, request):
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

class AllProducts(ListCreateAPIView):
    
    # overwrite the get queryset method for obtaining the queryset.. 
    # ( we are told to never get the query set direct)
    
    def get_queryset(self):
        return Product.objects.select_related('category').all()[:5]
    
    def get_serializer_class(self):
        return ProductSerializer
    
    def get_serializer_context(self):
        return {'request':self.request}



notes = """

retrieve the object and pass it to the serializer


"""

@api_view(['GET', 'PUT', 'DELETE'])
def product_details(request,id):
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

class ProductDetails_OLD(APIView):
    
        
    def get(self, request, id):
        # get the product you want to work with 
        product = get_object_or_404(Product, pk=id)
        # serialisze it using the responsible serializer
        serializer = ProductSerializer(product)
        # get the data from it and pass it and pass it as a response
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)
    
    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data = request.data, )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        
        # check if it has order items associated with it
        if product.orderitems.count()>0:
            return Response(data={'error':'Product cant be deleted because it is associated to an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductDetails(RetrieveUpdateDestroyAPIView):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'id'
    
    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        
        # check if it has order items associated with it
        if product.orderitems.count()>0:
            return Response(data={'error':'Product cant be deleted because it is associated to an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])
def category_list(request):
    
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

class CategoryList(ListCreateAPIView):
    
    def get_queryset(self):
        
        qry_set = ( Category.objects
        .annotate( product_count = Count('product_category'))
        .all()
        )
        return qry_set
    
    def get_serializer_class(self):
        return CategorySerializer
    
    def get_serializer_context(self):
        return {'request': self.request}
    

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

class CategoryDetail(RetrieveUpdateDestroyAPIView):
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # lookup_field = 'id'
    
    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        
        # check if it has order items associated with it
        if category.product_category.count()>0:
            return Response(data={'error':'Category cant be deleted because it is associated products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
