from django.shortcuts import render
from .models import Profile

# Create your views here.

'''
Get all users
'''
def profiles(request):
    profiles = Profile.objects.all()  # Retrieve all the profiles in the db / model - QuerySet object
    context = {'profiles':profiles}
    return render(request, 'usersApp/profiles.html', context)


'''
Get the specific user
'''
def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    
    skills_with_description =  profile.skill_set.exclude(description__exact="") # child model - profile.skill_set + if the skill does not have a description exclude it / filter it out!
    skills_no_description = profile.skill_set.filter(description="") # Every skill that has an empty string for the description, give it back!
    
    context = {'profile':profile, 'topSkills': skills_with_description, 'otherSkills': skills_no_description}
    return render(request, 'usersApp/user-profile.html', context)