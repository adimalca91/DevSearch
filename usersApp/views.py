from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required     # This decorator will simply sit above any view that we want to block and basically require athentication for
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Profile, Skill, Message
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import searchProfiles, paginateProfiles

# Create your views here.

'''
Get all users
'''
def profiles(request):
    profiles, search_query = searchProfiles(request)
    
    custom_range, profiles = paginateProfiles(request, profiles,3) # paginate 3 profiles at a time
    
    context = {'profiles':profiles, 'search_query':search_query, 'custom_range':custom_range}
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
        username = request.POST['username'].lower()
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
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
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

@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    
    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill was deleted successfully!")
        return redirect('account')
    
    
    context = {'object':skill}
    return render(request, 'delete_template.html', context)
    

  
@login_required(login_url='login')   
def inbox(request):
    profile = request.user.profile  # Get the currently logged-in user
    messageRequests = profile.messages.all()   # This is b/c the 'related_name' attribute in the Message model - in order to get a profile's messages, as in the messages sent to this owner / profile
    unreadCount = messageRequests.filter(is_read=False).count()
    
    context = {'messageRequests':messageRequests, 'unreadCount':unreadCount}
    return render(request,'usersApp/inbox.html',context)

@login_required(login_url='login') 
def viewMessage(request, pk):
    profile = request.user.profile  # Get the currently logged-in user
    message = profile.messages.get(id=pk) # Query the profile itself to get the messages, ensure that users can't access someone else's message by just accessing that pk
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message':message}
    return render(request,'usersApp/message.html',context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    
    # Check if the user is logged-in or not
    try:
        sender = request.user.profile
    except:
        sender = None
        
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            
            if sender:
                message.name = sender.name
                message.email = sender.email
            
            message.save()
            
            messages.success(request, "Your message was successfully sent!")
            return redirect('user-profile', pk=recipient.id)  # If i send someone a msg i will be redirected to their account 
            
    context = {'recipient':recipient, 'form':form}
    return render(request,'usersApp/message_form.html', context)