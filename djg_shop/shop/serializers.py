from decimal import Decimal
from rest_framework import serializers

from .models import Product, Category


notes = """

serializers have field names just like the models fields

you fields that arent in your application
describe a funtion to get the result and use method field and pass the function

renaming fields, you can rename fields and state the source name from the model

you can include related models

"""

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    category_name = serializers.CharField(max_length=255)

class ProductSerializer(serializers.ModelSerializer):
    
    
    # category = serializers.HyperlinkedRelatedField(
    #     queryset = Category.objects.all(),
    #     view_name = 'category-detail'        
    # )
    
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField('calculate_tax')
    
    
    # py default model serializers use pk field for relations
    
    # you can always retain modifications
    
    class Meta:
        model = Product
        fields = [ 'id', 'product_name', 'unit_price', 'category', 'price_with_tax', 'slug', 'inventory', 'product_description' ]
        
        # this is a bad practice so i hear
        # fields = '__all__' 



    
    
    
    # id = serializers.IntegerField()
    # product_name = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    
    # # you can calculate new fields
    # price_with_tax = serializers.SerializerMethodField('calculate_tax')
    
    # # this returns id
    # category = serializers.PrimaryKeyRelatedField( queryset = Category.objects.all())
    
    # # this returns the real name of category -- this has to be same name as field -- unless you do source source='category' 
    # category = serializers.StringRelatedField() 
    
    # # you can even return a whole object by another serializer --- nesting
    # category = CategorySerializer()
    
    # # setting it as a link back home to categories
    # category = serializers.HyperlinkedRelatedField(
    #     queryset = Category.objects.all(),
    #     view_name = 'category-detail'        
    # )
    
    
    def calculate_tax(self, product:Product):
        return product.unit_price * Decimal(1.1)


