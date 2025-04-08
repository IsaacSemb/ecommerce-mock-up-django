# django apps
from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count, Avg, Max, Min, Sum
from django.db.models import Value, F, Func

# django filter
from django_filters.rest_framework import DjangoFilterBackend

# restframework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.mixins import ListModelMixin, CreateModelMixin 
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView 
from rest_framework.viewsets import ModelViewSet



# personal imports
from .models import Category, OrderItem, Product, Review
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer



# combining multiple related views into a single view set
# example the product and product details

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return { 'product_id' : self.kwargs['product_pk'] }
    
    

class ProductViewSet(ModelViewSet):
    """
    this combines all products views  
    the one that get all products  
    and the one that gets a single product
    """
    # both have getting a query set that is the same
    
    # queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category_id']
    
    def get_queryset(self):
        return Product.objects.all()
        
        category_id = self.request.query_params.get('category_id')
        
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset
    
    # both use the product serializer class
    def get_serializer_class(self):
        return ProductSerializer
    
    # all need context
    def get_serializer_context(self):
        return {'request':self.request}
    
    def delete_old(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        
        # check if it has order items associated with it
        if product.orderitems.count()>0:
            return Response(data={'error':'Product cant be deleted because it is associated to an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count()>0:
            return Response(data={'error':'Product cant be deleted because it is associated to an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)

class CategoryViewSet(ModelViewSet):
    """
    this combines all Categories views  
    the one that get all Categories  
    and the one that gets a single Category
    """
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    # both have getting a query set that is the same
    def get_queryset(self):
        
        qry_set = ( Category.objects
        .annotate( product_count = Count('product_category'))
        .all()
        )
        return qry_set
    
    # both use the Category serializer class
    def get_serializer_class(self):
        return CategorySerializer
    
    # all need context
    def get_serializer_context(self):
        return {'request':self.request}
    
    def delete_old(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        
        # check if it has order items associated with it
        if category.product_category.count()>0:
            return Response(data={'error':'Category cant be deleted because it is associated products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, *args, **kwargs):
        # check if it has order items associated with it
        
        category = get_object_or_404(Category, pk=kwargs['pk'])
        
        # check if it has order items associated with it
        if category.product_category.count()>0:
            return Response(data={'error':'Category cant be deleted because it is associated products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
        return super().destroy(request, *args, **kwargs)



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
        return Product.objects.all()
    
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

class ProductDetail(RetrieveUpdateDestroyAPIView):
    
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
