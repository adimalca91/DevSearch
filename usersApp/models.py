from django.db import models
from django.contrib.auth.models import User
import uuid

from django.db.models.signals import post_save  # This method is going to be triggered / invoked any time a model is saved already and after it's saved!
from django.db.models.signals import post_delete
from django.dispatch import receiver

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
    username = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
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
    
    def __str__(self):
        return str(self.username)
    
    

class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True) # A user / profile can have many skills
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return self.name
    
    
# Django Signals
'''
Create some reciever and sender that will fire off anytime the save() method is called on a user profile
'''

'''
Arguments:
sender - The model that actually sends this
instance - The instance of the model that actually triggered this (the object)
created - Boolean that lets us know if a user / a model was added to the db or if it was simply saved again
        - lets us know if a new record in the db was added or not.
'''
#@receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
            )

'''
Anytime we delete a profile we also want to delete a user
Note - when delete is called on a user instance then it automatically deletes the user's profile b/c the 
one-to-one CASCASDE relationship!
But, if the profile gets deleted then now with this method, the user associated with that profile 
also gets deleted!
'''
@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    user = instance.user    # the instance here is a Profile instance - so instance.user is the user associated with that profile!
    user.delete()

# Any time a user model instance gets created a profile will be created
# Any time a user gets created what do we want to do?
post_save.connect(createProfile, sender=User)


post_delete.connect(deleteUser, sender=Profile)