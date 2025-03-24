from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class Tag(models.Model):
    tag_name = models.CharField(verbose_name='name of the tag', max_length=255)
    

notes_taggedItem = """
    for tagged object we cdant just import say products 
    cause the a dependency will be created between the two apps (shop and tags)
    we can use a generic model called content type from the Content type class   
    
    object_model_id --- content_type
        django assigns an ID to all models once they are created and migrated
        so it uses this id to look through them
        
    id_of_exact_object ---- object_id 
        once django finds the mdel in the object model id
        it then goes in and looks for the exact object
    
    target_object_obtainer ----- content_object
        this combines the above 2 to obtain the object from its model

"""
    
class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, verbose_name="which tag", on_delete=models.CASCADE)
    object_model_id_in_django = models.ForeignKey(ContentType, verbose_name='internal model id which object belongs', on_delete=models.CASCADE)
    id_of_exact_object = models.PositiveIntegerField(verbose_name='ID of exact object in the model')
    target_object_obtainer = GenericForeignKey( ct_field='object_model_id_in_django', fk_field='id_of_exact_object' )