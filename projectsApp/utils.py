'''
This file will contain helper functions
'''

from .models import Project, Tag
from django.db.models import Q


def searchProjects(request):
    search_query = ""
    
    # Check if something was searched in the search bar
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
    tags = Tag.objects.filter(name__icontains=search_query)  # The project model has a tags field which is many-to-many field
    
    # projects = Project.objects.all()  # QuerySet - dictionary like object
    
    # distinct() to prevent duplicates!
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) | # here we go one level up and we query by the parent item. 
        # we go into the parent object (owner) and then into the attribute of 'name'
        # give us every project where the owner's name contains 'search_query'
        Q(tags__in=tags)
    )
    
    return(projects, search_query)