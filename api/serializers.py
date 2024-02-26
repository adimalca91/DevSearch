# We need to serialize data before we return it
# Take python models and serialize them

# Serialization is the process of converting our data - those python objects will be converted to Json objects

# Here we will work with Model Serialization

from rest_framework import serializers
from projectsApp.models import Project


'''
This is a Model Serializer - it will take the Project Model and will serialize it (convert it) into a Json object
'''
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'