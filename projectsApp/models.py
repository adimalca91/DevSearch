from django.db import models
import uuid

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=200)   # By default null=False - required to enter data in this field (for the database)
    description = models.TextField(null=True, blank=True)  # Does NOT require to enter data in this field! blank is the same but for django form to be submitted! We can submit a form without adding this!
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg") # B/c its in "images" folder no need to specify path, otherwise path needed
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)  # The tag can be connected to many models
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    
    def __str__(self):
        return self.title
    
'''
One-to-Many relationship because one project can have many reviews!
'''
class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
        )
    # owner = 
    project = models.ForeignKey(Project, on_delete=models.CASCADE) # Foreign key to create the connection to the Project model
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)    # Drop-down list
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return self.value
    

'''
Many-to-Many relationship.
One project can have many Tags and a Tag can have meny projects
'''
class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return self.name
    
        
    
    
    
    
    
