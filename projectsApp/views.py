from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required     # This decorator will simply sit above any view that we want to block and basically require athentication for
from .models import *
from .forms import *
from django.db.models import Q
from .utils import searchProjects, paginateProjects
from django.contrib import messages


# Create your views here.

'''
This is a view page that displays all of the projects
Pass in some dynamic data to the template to render and display in the browser
'''
def projects(request):
    
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6) # Allow for 6 projects to show in one page
    
    context = {'projects': projects, 'search_query':search_query,'custom_range':custom_range}
    return render(request, 'projectsApp/projects.html', context)

'''
This is a view page to display a single project.
When we have a list of projects we want to open up a project and learn about it.
We want to read about this specific project.
This is a Dynamic view function.
Recall that this pk is UUID 
'''
def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    # tags = projectObj.tags.all() # QuerySet - dict-like object of tag objects
    form = ReviewForm()
    
    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)  # Get the instance of the Review 
        review.project = projectObj
        review.owner = request.user.profile
        review.save()
        
        # Update project votecount
        projectObj.getVoteCount    # The property decorator enables us to run it like that (as an attribute) and not as a method
        
        messages.success(request, 'Your review was successfully submitted')
        return redirect('project', pk=projectObj.id)   # redirect with a dynamic value
        
    context = {'projectObject': projectObj, 'form':form}
    return render(request, 'projectsApp/single-project.html', context)

'''
CRUD - CREATE, READ, UPDATE, DELETE -OPERATIONS! 
'''

# ADI - on order to create something we need a FORM !!!
# Create and Read - Create any kind of project via it's form - hence NO pk paramater
# This decorator will simply sit above any view that we want to block and basically require athentication for
# In order to view this createProject page the decorator requires that the user will be logged-in! If the user is NOT logged in then send the user to the login page (according to parameter)
@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile  # get the currently logged-in user
    form = ProjectForm()
    
    if request.method == "POST":
        newtags = request.POST.get('newtags').replace(",", " ").split()
        form = ProjectForm(request.POST, request.FILES)  # populate the form with the post data and FILES the user submitted in the form
        if form.is_valid():
            project = form.save(commit=False)   # Get the instance of the project w/o saving it in the DB yet! This gives us an instance of that current project
            project.owner = profile             # Update that owner attribute (one-to-many relationship)
            project.save()                      # CREATE A PROJECT OBJECT IN THE PROJECT MODEL / SAVES TO THE PROJECT DB
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)   # access a project's object many-to-many relationship with tags
            return redirect('account')
        
    context = {'form':form}
    return render(request, 'projectsApp/project_form.html', context)

# Update and Read - Update a certain specific project via it's form - hence the pk parameter
@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile  # get the currently logged-in user
    project = profile.project_set.get(id=pk)   # Query ONLY that user's profiles - all the projects of that user!
    form = ProjectForm(instance=project)   # MUST pass in an instance of the project that we want to edit!
    
    if request.method == "POST":
        newtags = request.POST.get('newtags').replace(",", " ").split()
        # print("DATA: ", newtags) # QueryDict
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()       # CREATE A PROJECT OBJECT IN THE PROJECT MODEL - Update it with the new data
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)   # access a project's object many-to-many relationship with tags
            return redirect('account')
        
    context = {'form':form, 'project':project}
    return render(request, 'projectsApp/project_form.html', context)

# Delete - Delete a certain specific project via it's form - hence the pk parameter
@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile  # get the currently logged-in user
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()      # This will delete the project object from the DB / Model   
        return redirect('projects') 
    context = {'object' : project}
    return render(request, 'delete_template.html', context)
    
    
