from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required     # This decorator will simply sit above any view that we want to block and basically require athentication for
from django.contrib import messages
from django.contrib.auth.models import User
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


'''
In this process, when a user submits their data we want to output certain errors if things go wrong
'''

def loginUser(request):
    
    # restrict a logged in user from directly going to '/login' path in the url bar
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == "POST":
        print(request.POST) # QueryDict object
        username = request.POST['username']
        password = request.POST['password']
        
        
        try:                                                   # Check if the user exists
            user = User.objects.get(username=username)
        except:                                                # if the user does NOT exist
            # print("Username does not exist")
            messages.error(request, "Username does not exist")  # flash message - one time message when page is rendered
            
        # Takes in the username and password and will make sure that the password matches the username and returns either the user instance or None - Query the db, if finds a user that matches the username and password then it will return back that user
        user = authenticate(request, username=username, password=password)
        
        # If the user does exists!
        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:                                             # user exists but can't login - if user did not exist then it would print in the except section
            # print("Username OR password is incorrect")
            messages.error(request, "Username OR password is incorrect")
            
    return render(request, 'usersApp/login_register.html')


def logoutUser(request):
    logout(request)
    messages.error(request, "User was successfully logged out")
    return redirect('login')
    
    