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
    
    
    class Meta:
        # ordering = ['created'] # Order projects oldest to newest (for newst to oldest do '-created')
        ordering = ['created']
    
    
    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url
    
    

class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True) # A user / profile can have many skills
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return self.name
    
    
class Message(models.Model):
    # SET_NULL - if I send a message to xomeone and I delete my account I want the recipient to still
    #            see that message, I don't want it to go away, they shpuld have a record of it.
    # null=true - users that don't have an account can't send messages - we will NOT always have a sender attribute here
    # blank=true - a form could be submitted without a sender / a person with NO account can't send messages
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    
    # To access the profiles messages, instead of doing 'profile.message_set' we will just be able to type in
    # 'messages'. This is how that profile model is giong to connect to this. We need to add this to one of these
    # fields at least b/c otherwise it will not allow us to have a connection to the profile model twice! B/c both
    # 'sender' and 'recipient' are connected to Profile then to know to which one we want to get we need the related_name
    # to differentiate b/w the two fields
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return self.subject
    
    class Meta:
        ordering = ['is_read', '-created']