from django.contrib import admin
from . import models

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
    list_display = ['product_name', 'unit_price']


admin.site.register(models.Category)



