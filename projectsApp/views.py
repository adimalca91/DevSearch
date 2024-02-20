from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required     # This decorator will simply sit above any view that we want to block and basically require athentication for
from .models import *
from .forms import *
from django.db.models import Q
from .utils import searchProjects
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

'''
This is a view page that displays all of the projects
Pass in some dynamic data to the template to render and display in the browser
'''
def projects(request):
    
    projects, search_query = searchProjects(request)
    
    page = request.GET.get('page')  # Needs to have a search parameter! "projects/?page=xxx" - page is the search parameter!
    results = 3
    paginator = Paginator(projects, results)
    
    try:
        # Reset the projects variable with pagination - get the first page out of the 3 page projects
        projects = paginator.page(page)
    except PageNotAnInteger:
        # If a page is NOT passed in - set the page to 1 - the first load
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        # If a user tries to go to a page with no results - a page that we don't have!
        page = paginator.num_pages   # returns the number of pages we have
        projects = paginator.page(page)  # return the last page
        
    left_index = (int(page) - 4)
    
    if left_index < 1:
        left_index = 1
        
    right_index = (int(page) + 5)
    
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1
    
    custom_range = range(left_index, right_index)
    
    context = {'projects': projects, 'search_query':search_query, 'paginator':paginator, 'custom_range':custom_range}
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
    context = {'projectObject': projectObj}
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
        form = ProjectForm(request.POST, request.FILES)  # populate the form with the post data and FILES the user submitted in the form
        if form.is_valid():
            project = form.save(commit=False)   # Get the instance of the project w/o saving it in the DB yet! This gives us an instance of that current project
            project.owner = profile             # Update that owner attribute (one-to-many relationship)
            project.save()                      # CREATE A PROJECT OBJECT IN THE PROJECT MODEL / SAVES TO THE PROJECT DB
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
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()       # CREATE A PROJECT OBJECT IN THE PROJECT MODEL - Update it with the new data
            return redirect('account')
        
    context = {'form':form}
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
    
    
