'''
This file will contain helper functions
'''

from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProfiles(request, profiles, results):

    page = request.GET.get('page')  # Needs to have a search parameter! "profiles/?page=xxx" - page is the search parameter!
    # results = 3
    paginator = Paginator(profiles, results)
    
    try:
        # Reset the profiles variable with pagination - get the first page out of the 3 page profiles
        profiles = paginator.page(page)
    except PageNotAnInteger:
        # If a page is NOT passed in - set the page to 1 - the first load
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        # If a user tries to go to a page with no results - a page that we don't have!
        page = paginator.num_pages   # returns the number of pages we have
        profiles = paginator.page(page)  # return the last page
    
    left_index = (int(page) - 4)    # to show 5 button pages at a time
    # left_index = (int(page) - 1)
    
    if left_index < 1:
        left_index = 1
    
    right_index = (int(page) + 5)   # to show 5 button pages at a time
    # right_index = (int(page) + 2)     # to show 3 button pages at a time
    
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1
    
    custom_range = range(left_index, right_index)
    
    return custom_range, profiles




def searchProfiles(request):
    
    search_query = ""
    
    # Check if something was searched in the search bar
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
    # print('SEARCH:', search_query)
    
    # we only want to search our skiils if that query matches perfectly - its a QuerySet of skills
    # skills = Skill.objects.filter(name__iexact=search_query)
    
    skills = Skill.objects.filter(name__icontains=search_query)
    
    # profiles = Profile.objects.all()  # Retrieve all the profiles in the db / model - QuerySet object
    # if its an empty string we'll get back all profiles in the db b/c all profiles contain something (the emptystring),
    # but if it contains something it will filter
    # lookup the profile by either the name OR the short_intro fields
    # distinct added b/c there are diplicates due to skills - ADI: i think it loops over the skills queryset and
    # for every skill in skills it filter by it - now the empty string is in every string (in the empty way) therefore it 
    # displays the profile with duplicates for every skill.
    profiles = Profile.objects.distinct().filter(Q(name__icontains=search_query) |   # without case sensitivity - name is a profile field and __icontains is a filter on it
                                      Q(short_intro__icontains=search_query) |
                                      Q(skill__in=skills))     # We want to know - does the profile have a skill that is listed in this skills QuerySet  
    
    return profiles, search_query
    