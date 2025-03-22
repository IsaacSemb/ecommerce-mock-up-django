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
    pass



class CartItem(models.Model):
    pass



class Order(models.Model):
    pass



class OrderItem(models.Model):
    pass


