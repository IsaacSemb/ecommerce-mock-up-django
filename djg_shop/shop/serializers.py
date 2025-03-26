from rest_framework import serializers


notes = """

serializers have field names just like the models fields


"""

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product_name = serializers.CharField(max_length=255)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)


