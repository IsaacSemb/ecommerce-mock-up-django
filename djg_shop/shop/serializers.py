from decimal import Decimal
from rest_framework import serializers

from .models import Cart, CartItem, Product, Category, Review


notes = """

serializers have field names just like the models fields

you fields that arent in your application
describe a funtion to get the result and use method field and pass the function

renaming fields, you can rename fields and state the source name from the model

you can include related models

"""






class CategorySerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # category_name = serializers.CharField(max_length=255)
    
    # product_counter = serializers.SerializerMethodField('get_product_count')
    product_count = serializers.IntegerField(read_only=True)
        
    class Meta:
        model = Category
        fields = [ 'id', 'category_name', 'category_description','product_count'] #, 'product_counter' ]
    
    def get_product_count(self, category: Category ):
        return category.product_category.count()
        
        

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
    
    
    # if you need to overwrite the validate function you can
    # def validate(self, attrs):
    #     return super().validate(attrs)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        # fields = '__all__'
        fields = ['reviewer', 'description', 'date']
        
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'unit_price']
    
class cartItemSerializer(serializers.ModelSerializer): 
    
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField('get_total_price')
    
    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    
    id = serializers.UUIDField(read_only=True)
    items = cartItemSerializer(many=True)
    grand_total = serializers.SerializerMethodField('get_grand_total')
    
    def get_grand_total(self, cart: Cart):
        return sum([ cart_item.quantity * cart_item.product.unit_price for cart_item  in cart.items.all() ])
        
    
    class Meta:
        model = Cart
        fields = [ 'id', 'items', 'grand_total' ]