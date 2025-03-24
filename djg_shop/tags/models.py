from django.db import models

# Create your models here.

class Tag(models.Model):
    label = models.CharField(verbose_name='tag label', max_length=255)
    
    
class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, verbose_name="which tag", on_delete=models.CASCADE)
        
