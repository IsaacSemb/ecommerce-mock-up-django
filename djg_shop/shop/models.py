from django.db import models

# Create your models here.

notes_product = """

- text field doesnt need max length
- verbose name means human readable name hence it is optional

- auto_now_add : records on only first save
- auto_now : records on only save


"""

class Product(models.Model):
    product_name = models.CharField(verbose_name='Product Name', max_length=255)
    description = models.TextField(verbose_name= "Product Description")
    unit_price = models.DecimalField(verbose_name="Unit Price", max_digits=6, decimal_places=2)
    inventory = models.IntegerField(verbose_name="inventory")
    created_at = models.DateTimeField(verbose_name="date and time created", auto_now_add=True)
    last_update = models.DateTimeField(verbose_name="date and time updated", auto_now=True)
    
    





class Customer(models.Model):
    pass



class Category(models.Model):
    pass



class Address(models.Model):
    pass



class Cart(models.Model):
    pass



class CartItem(models.Model):
    pass



class Order(models.Model):
    pass



class OrderItem(models.Model):
    pass


