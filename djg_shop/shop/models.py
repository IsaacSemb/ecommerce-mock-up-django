from uuid import uuid4
from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from django.contrib import admin

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
    product_description = models.TextField(verbose_name= "Product Description")
    unit_price = models.DecimalField(verbose_name="Unit Price", max_digits=6, decimal_places=2)
    inventory = models.IntegerField(verbose_name="inventory")
    created_at = models.DateTimeField(verbose_name="date and time created", auto_now_add=True)
    last_update = models.DateTimeField(verbose_name="date and time updated", auto_now=True)
    category = models.ForeignKey('Category', verbose_name="Product Category", on_delete=models.PROTECT, related_name='product_category')
    slug = models.SlugField()
    
    def __str__(self): 
        return self.product_name
    
    class Meta:
        ordering = ['product_name']
        


notes_product = """

- you can null a field with the null parameter
- you can make a field unique

"""

class Customer(models.Model):
    
    MEMBERSHIP_BASIC = 'B'
    MEMBERSHIP_PREMIUM = 'P'
    
    MEMBERSHIP_TIERS = [
        (MEMBERSHIP_BASIC, 'Basic'),
        (MEMBERSHIP_PREMIUM, 'Premium')
    ]
    
    # these have been added in the user app model
    # first_name = models.CharField(verbose_name="First Name", max_length=255) 
    # last_name = models.CharField(verbose_name="Last Name", max_length=255) 
    # email = models.EmailField(verbose_name='Customer Email Address', max_length=255, unique=True)
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(verbose_name="Phone Number", max_length=20)
    date_of_birth = models.DateField(verbose_name="Date of Birth", null=True)
    created_at = models.DateTimeField(verbose_name="date and time created", auto_now_add=True)
    membership = models.CharField(verbose_name="Membership Tier", max_length=1, choices=MEMBERSHIP_TIERS, default=MEMBERSHIP_BASIC)
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
        
    
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
    
    class Meta:
        ordering = [ 'user__first_name', 'user__last_name']



class Category(models.Model):
    category_name = models.CharField( verbose_name="category name", max_length=255)
    category_description = models.TextField(verbose_name="Category Description", null=True) 
    
    # slug ??
    # slug = models.SlugField(verbose_name="Slug", max_length=255, unique=True)
    
    # time stamps 
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.category_name
    
    class Meta:
        ordering = ['category_name']

    


notes_address = """

- for a one to one relationship, the first argument has no keyword ( not sure )
- you can name the model direct like below

- but if the model is not in the same app the you do <app.model> in our case --> 'shop.Customer'

- also since python reads up to down if the child comes before the parent, we use the class name in string form
eg --->  ( 'Customer', verbose.... )

- set primary key so that there cant be 2 customers

"""

class Address(models.Model):
    street = models.CharField(verbose_name="Street Name", max_length=255)
    city = models.CharField(verbose_name="City Name", max_length=255)
    country = models.CharField(verbose_name="Country of Residence", max_length=255)
    postal_code = models.CharField(verbose_name="Postal Code", max_length=20)
    is_default = models.BooleanField(verbose_name="default address", default=False)
    customer = models.ForeignKey(Customer, verbose_name="Owner of address", on_delete=models.CASCADE)


class Cart(models.Model):
    id = models.UUIDField(verbose_name='Cart ID', primary_key=True, default=uuid4)
    created_at = models.DateTimeField(verbose_name="date and time created", auto_now_add=True)
    # customer = models.OneToOneField( Customer, verbose_name="Cart Owner", on_delete=models.CASCADE, primary_key=True)


class CartItem(models.Model):
    quantity = models.PositiveSmallIntegerField(verbose_name="Quantity of all Items", validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(verbose_name="date and time created", auto_now_add=True)
    cart = models.ForeignKey(Cart, verbose_name="which Cart", on_delete=models.CASCADE, related_name='items')
    product = models.OneToOneField(Product, verbose_name="which product", on_delete=models.CASCADE)
    cart_item_description = models.TextField(verbose_name= "Cart Item Description", null=True)
    
    class Meta:
        unique_together = [
            ['cart', 'product']
        ]

    # price at time -- pricess keep change?? --- on order item


class Order(models.Model):
    
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETED = 'C'
    PAYMENT_FAILED = 'F'
    
    
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_PENDING, 'pending'),
        (PAYMENT_COMPLETED,'complete'),
        (PAYMENT_FAILED, 'failed')
    ]
    
    total_amount = models.DecimalField(verbose_name="Total Amount for Order", max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(verbose_name="date and time created", auto_now_add=True)
    payment_status = models.CharField(verbose_name="payment status",max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_PENDING)
    customer = models.ForeignKey(Customer, verbose_name="Ordered by", on_delete=models.PROTECT)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # from which cart ??? seems illogical
    
    # def __str__(self):
    #     pass
    
    class Meta:
        permissions = [
            ('cancel_order', 'can cancel an order')
        ]



class OrderItem(models.Model):
    unit_price = models.DecimalField(verbose_name="Unit Price", max_digits=6, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(verbose_name="Quantity of Items")
    created_at = models.DateTimeField(verbose_name="date and time created", auto_now_add=True)
    order = models.ForeignKey( Order, verbose_name="Which Order", on_delete=models.CASCADE )
    product = models.ForeignKey( Product, verbose_name="Which product", on_delete=models.PROTECT, related_name='orderitems' )


class Review(models.Model):
    product = models.ForeignKey(Product,verbose_name='which order', on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    
    
    