from django.contrib import admin
from . import models

admin_notes = """
the admin file is for when you want to custromise 
how your models will look in the admin site

__str method changes how you see the objects
instead of seeing the Object(id)  you see the real name 
"""

# Register your models here.

admin.site.register(models.Category)
