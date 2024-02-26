from django.http import JsonResponse     # Takes any python data that we have, and will turn it into json data
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response 
from .serializers import ProjectSerializer
from projectsApp.models import Project


# A view that will tell us all the url paths / toutes that we are going to have inside of our api's
# Kind of like documentation for api

@api_view(['GET'])  # specify this as a GET method
def getRoutes(request):
    
    # A list of python dicts that will later turn to JS objects
    # This python list full of dicts will turn into a javascript array full of objects
    routes = [
        {'GET':'/api/projects'},              # This will return back a list of project objects
        {'GET':'/api/projects/id'},           # This will return back a single project object
        {'POST':'/api/projects/id/vote'},
        
        {'POST':'/api/users/token'},          # Jason web tokens
        {'POST':'/api/users/token/refresh'},
    ]
    
    return Response(routes)                     # JsonResponse will give us Json data; safe - tells we can return back something that is more than just a py dict
                                               # By default the JsonResponse can only return back a py dict, but b/c we are sending a LIST of dicts we need to set safe to False - go ahead and turn any kind of data that we want into Json data

                                              
@api_view(['GET'])
def getProjects(request):
    print('USER: ', request.user)
    projects = Project.objects.all()                     # Query Project model to retrieve all the project objects
    serializer = ProjectSerializer(projects, many=True)  # Takes the queryset and turn it into json data; many - for serializing many objects
    return Response(serializer.data)


@api_view(['GET'])    
def getProject(request, pk):
    project = Project.objects.get(id=pk)                 # Query Project model to retrieve a single project object
    serializer = ProjectSerializer(project, many=False)  # Takes the queryset and turn it into json data; many - for serializing many objects
    return Response(serializer.data)