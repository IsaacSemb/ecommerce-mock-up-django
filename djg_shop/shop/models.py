from django.db import models

# Create your models here.

# stuff to remember
    
    # ABSTRACT CLASSES
    # you can create separate abstract classes for repeated attribute 
    # for exapmle a timestamped class for time stamping 


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
    
    # category
    # slug


notes_product = """

- you can null a field with the null parameter
- you can make a field unique

"""

class Customer(models.Model):
    first_name = models.CharField(verbose_name="First Name", max_length=255) 
    last_name = models.CharField(verbose_name="Last Name", max_length=255) 
    phone = models.CharField(verbose_name="Phone Number", max_length=20)
    email = models.EmailField(verbose_name='Customer Email Address', max_length=255, unique=True)
    date_of_birth = models.DateField(verbose_name="Date of Birth", null=True)
    created_at = models.DateTimeField(verbose_name="date and time created", auto_now_add=True)
    
    # address
    # membership



class Category(models.Model):
    category_name = models.CharField( verbose_name="category name", max_length=255)
    category_description = models.TextField(verbose_name="Category Description") 
    
    # slug ??
    # slug = models.SlugField(verbose_name="Slug", max_length=255, unique=True)
    
    # time stamps 
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    



class Address(models.Model):
    street = models.CharField(verbose_name="Street Name", max_length=255)
    city = models.CharField(verbose_name="City Name", max_length=255)
    country = models.CharField(verbose_name="Country of Residence", max_length=255)
    postal_code = models.CharField(verbose_name="Postal Code", max_length=20)
    is_default = models.BooleanField(verbose_name="default address", default=False)
    
    # customer



class Cart(models.Model):
    created_at = models.DateTimeField(verbose_name="date and time created", auto_now_add=True)
    
    # customer fk owner
    # 



class CartItem(models.Model):
    quantity = models.IntegerField(verbose_name="Quantity of Items")
    created_at = models.DateTimeField(verbose_name="date and time created", auto_now_add=True)
    
    # cart fk (from which cart)
    # what product (fk)
    # price at time -- pricess keep change



class Order(models.Model):
    total_amount = models.DecimalField(verbose_name="Total Amount for Order", max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(verbose_name="date and time created", auto_now_add=True)
    
    # who ordered customer fk
    # from which cart
    # status -- multiple choice for later
    



class OrderItem(models.Model):
    unit_price = models.DecimalField(verbose_name="Unit Price", max_digits=6, decimal_places=2)
    quantity = models.IntegerField(verbose_name="Quantity of Items")
    created_at = models.DateTimeField(verbose_name="date and time created", auto_now_add=True)
    
    # from what order id
    #  what product id



