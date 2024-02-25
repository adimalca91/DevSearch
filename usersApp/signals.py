from django.db.models.signals import post_save  # This method is going to be triggered / invoked any time a model is saved already and after it's saved!
from django.db.models.signals import post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile

from django.core.mail import send_mail
from django.conf import settings

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
    # print("Profile save triggered")
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )
        
        # send_mail(
        #     "Subject here",
        #     "Here is the message.",
        #     "from@example.com",
        #     ["to@example.com"],
        #     fail_silently=False,
        # )
        
        subject = "Welcome to DevSearch"
        message = "We are glad you are here!"
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )



'''
Connecting between the user and the profile - anytime a profile is editted then it's user data is also editted
and the opposite!
'''
def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    
    # Ensure its NOT the first time this user is created
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()
    


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
# This createProfile function is triggered when a User is saved!
post_save.connect(createProfile, sender=User)

post_save.connect(updateUser, sender=Profile)

post_delete.connect(deleteUser, sender=Profile)