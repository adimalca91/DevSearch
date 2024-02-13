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
    context = {'profile':profile}
    return render(request, 'usersApp/user-profile.html', context)