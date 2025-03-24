from django.db import models

# Create your models here.

class Tag(models.Model):
    tag_name = models.CharField(verbose_name='name of the tag', max_length=255)
    

notes_taggedItem = """
    for tagged object we cdant just import say products 
    cause the a dependency will be created between the two apps (shop and tags)
    we can use a generic model called content type from the Content type class   
    

"""
    
class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, verbose_name="which tag", on_delete=models.CASCADE)
        
