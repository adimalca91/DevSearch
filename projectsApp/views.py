from django.shortcuts import render
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

def createProject(request):
    form = ProjectForm()
    context = {'form':form}
    return render(request, 'projectsApp/project_form.html', context)
