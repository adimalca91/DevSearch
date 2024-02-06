from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

'''
This is a list of our projects
'''
def projects(request):
    return HttpResponse("Here are our projects")

'''
This is a single project.
When we have a list of projects we want to open up a project and learn about it.
We want to read about this specific project.
This is a Dynamic view function.
'''
def project(request, pk):
    return HttpResponse(f"SINGLE PROJECT {pk}")

