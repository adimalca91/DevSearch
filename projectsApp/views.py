from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

projectsList = [
    {'id':'1',
     'title': "E-commerce Website",
     'description': "Fully functional eccomerce website"
    },
    {'id':'2',
     'title': "Portfolio Website",
     'description': "This is a project where I built out my portfolio"
    },
    {'id':'3',
     'title': "Social Network",
     'description': "Awesome open source project I am still working on"
    }
]

'''
This is a list of our projects
Pass in some dynamic data to the template to render and display in the browser
'''
def projects(request):
    page = "projects"
    number = 10
    context = {'page':page, 'number': number, 'projects': projectsList}
    return render(request, 'projectsApp/projects.html', context)

'''
This is a single project.
When we have a list of projects we want to open up a project and learn about it.
We want to read about this specific project.
This is a Dynamic view function.
'''
def project(request, pk):
    projectObj = None
    for i in projectsList:
        if i['id'] == pk:
            projectObj = i
    context = {'projectObject': projectObj}
    return render(request, 'projectsApp/single-project.html', context)

