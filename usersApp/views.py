from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required     # This decorator will simply sit above any view that we want to block and basically require athentication for
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Skill
from .forms import CustomUserCreationForm, ProfileForm, SkillForm

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
    
    page = 'login'
    
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
            login(request, user)                          # creates a session based token in the db and adds it to the cookies
            return redirect('profiles')
        else:                                             # user exists but can't login - if user did not exist then it would print in the except section
            # print("Username OR password is incorrect")
            messages.error(request, "Username OR password is incorrect")
            
    return render(request, 'usersApp/login_register.html')


def logoutUser(request):
    logout(request)
    messages.info(request, "User was successfully logged out!")
    return redirect('login')

# Note - when register successfully a profile is automatically genretaed b/c we built signals for it!
def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # This will create a user object for us 
            user = form.save(commit=False)
            user.username = user.username.lower()   # make user that the username is lowercase
            user.save()                             # Now a user is officially being added to the db and saved
            
            messages.success(request, "User acount was successfully created!")
            
            login(request, user)     # The user will now be logged in
            
            return redirect('edit-account')
        
        else:
            messages.error(request, "An error has occured during registration")
    
    context = {'page':page, 'form':form}
    return render(request, 'usersApp/login_register.html', context)

@login_required(login_url='login')
def userAccount(request):
    # Get the logged-in user via request parameter - the one-to-one relationship
    profile = request.user.profile
    
    skills =  profile.skill_set.all()
    projects = profile.project_set.all()

    context = {'profile':profile, 'skills':skills, 'projects':projects}
    return render(request, 'usersApp/account.html', context)



@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile  # The logged-in user
    form = ProfileForm(instance=profile)  # pre-fill the fields with the current data
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    
    context = {'form':form}
    return render(request, 'usersApp/profile_form.html', context)
    
@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile  # b/c we excluded this field from the form the user fills up now we set it automatically to the associated logged-in user
            skill.save()
            messages.success(request, "Skill was added successfully!")
            return redirect('account')
        
    context = {'form':form}
    return render (request, 'usersApp/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)  # Ensure that ONLY the owner can edit his skill
    form = SkillForm(instance=skill)
    
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            skill.save()
            messages.success(request, "Skill was updated successfully!")
            return redirect('account')
        
    context = {'form':form}
    return render (request, 'usersApp/skill_form.html', context)


def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    
    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill was deleted successfully!")
        return redirect('account')
    
    
    context = {'object':skill}
    return render(request, 'delete_template.html', context)
    