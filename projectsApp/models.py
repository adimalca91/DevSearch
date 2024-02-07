from django.db import models
import uuid

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=200)   # By default null=False - required to enter data in this field (for the database)
    description = models.TextField(null=True, blank=True)  # Does NOT require to enter data in this field! blank is the same but for django form to be submitted! We can submit a form without adding this!
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    
    def __str__(self):
        return self.title
    
    
