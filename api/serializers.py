# We need to serialize data before we return it
# Take python models and serialize them

# Serialization is the process of converting our data - those python objects will be converted to Json objects

# Here we will work with Model Serialization

from rest_framework import serializers
from projectsApp.models import Project, Tag, Review
from usersApp.models import Profile


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

'''
This is a Model Serializer - it will take the Project Model and will serialize it (convert it) into a Json object
'''
class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()     # the method then has to start with 'get_'
    
    class Meta:
        model = Project
        fields = '__all__'
        
    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data