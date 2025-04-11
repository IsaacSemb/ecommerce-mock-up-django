from django.contrib import admin
from . import models
from django.db.models.aggregates import Count


admin_notes = """
the admin file is for when you want to custromise 
how your models will look in the admin site

__str method changes how you see the objects
instead of seeing the Object(id)  you see the real name 
"""

# Register your models here.


# custom admin manipulation for the product admin page
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'unit_price', 'inventory', 'inventory_status','category', 'category_description']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['category']
    
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory<10:
            return 'Low'
        return 'Ok'
    
    def category_description(self, product):
        return product.category.category_description


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [ 'category_name', 'product_count' ]

    @admin.display(ordering='counted_products')   
    def product_count(self, category):
        return category.counted_products # but this doesnt exist in the products so we have to create it
    
    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .annotate( counted_products=Count('product_category'))
            )


# might sound like common sense but
# to make something editable it has to be displayed first lol

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [ 'first_name', 'last_name', 'phone', 'date_of_birth', 'membership']
    list_editable = ['membership']
    list_per_page = 10 


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'customer', 'payment_status']
    list_per_page = 10
