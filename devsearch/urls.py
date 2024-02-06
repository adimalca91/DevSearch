"""
URL configuration for devsearch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', projects, name="projects"),
    path('project/<str:pk>/', project, name="project"),
]
