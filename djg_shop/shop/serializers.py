from decimal import Decimal
from rest_framework import serializers

from .models import Product


notes = """

serializers have field names just like the models fields

you fields that arent in your application
describe a funtion to get the result and use method field and pass the function

renaming fields, you can rename fields and state the source name from the model

"""

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product_name = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField('calculate_tax')
    
    def calculate_tax(self, product:Product):
        return product.unit_price * Decimal(1.1)


