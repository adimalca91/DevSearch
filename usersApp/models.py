from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

'''
Every User in the User db has one profile and every profile has one user!
The profile will get automatically generated any time we create a user!
Also, when a User is deleted it's associated profile also gets deleted.
'''
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(blank=True, null=True, upload_to="profiles/",
                                      default="profiles/user-default.png") # This will go in static/images folder and then in profiles folder and upload my pictures here. Again - we are uploading to the profiles folder and also getting the defualt from the profiles folder
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    
