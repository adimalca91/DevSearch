from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *

# Create your views here.

'''
This is a list of our projects
Pass in some dynamic data to the template to render and display in the browser
'''
def projects(request):
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(request, 'projectsApp/projects.html', context)

'''
This is a single project.
When we have a list of projects we want to open up a project and learn about it.
We want to read about this specific project.
This is a Dynamic view function.
'''
def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    # tags = projectObj.tags.all()
    context = {'projectObject': projectObj}
    return render(request, 'projectsApp/single-project.html', context)

'''
CRUD - CREATE, READ, UPDATE, DELETE -OPERATIONS! 
'''

# Create and Read - Create any kind of project via it's form - hence NO pk paramater
def createProject(request):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)  # populate the form with the post data and FILES the user submitted in the form
        if form.is_valid():
            form.save()       # CREATE A PROJECT OBJECT IN THE PROJECT MODEL / SAVES TO DB
            return redirect('projects')
        
    context = {'form':form}
    return render(request, 'projectsApp/project_form.html', context)

# Update and Read - Update a certain specific project via it's form - hence the pk parameter
def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)   # MUST pass in an instance of the project that we want to edit!
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()       # CREATE A PROJECT OBJECT IN THE PROJECT MODEL - Update it with the new data
            return redirect('projects')
        
    context = {'form':form}
    return render(request, 'projectsApp/project_form.html', context)

# Delete - Delete a certain specific project via it's form - hence the pk parameter
def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == "POST":
        project.delete()      # This will delete the project object from the DB / Model   
        return redirect('projects') 
    context = {'object' : project}
    return render(request, 'projectsApp/delete_template.html', context)
    
    
