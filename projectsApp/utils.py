'''
This file will contain helper functions
'''

from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProjects(request, projects, results):

    page = request.GET.get('page')  # Needs to have a search parameter! "projects/?page=xxx" - page is the search parameter!
    # results = 3
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
    
    left_index = (int(page) - 4)    # to show 5 button pages at a time
    # left_index = (int(page) - 1)
    
    if left_index < 1:
        left_index = 1
    
    right_index = (int(page) + 5)   # to show 5 button pages at a time
    # right_index = (int(page) + 2)     # to show 3 button pages at a time
    
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1
    
    custom_range = range(left_index, right_index)
    return custom_range, projects

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