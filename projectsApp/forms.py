from django.forms import ModelForm
from django import forms
from .models import Project, Review

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'featured_image' ,'demo_link', 'source_link']
        widgets = {
            'tags' : forms.CheckboxSelectMultiple(),
            } # A way to customize classes
        
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)  # Tell it which class (css class!) we're modifying
        
        # loop over the form and add the css class 'input' to every field
        # loop through every single field and add a css class of 'input'
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
            
        # self.fields['title'].widget.attrs.update({'class':'input', 'placeholder': 'Add title'})   # This is a css class! We are selecting the css attributes we want to modify
        
        # self.fields['description'].widget.attrs.update({'class':'input'})
        
    
class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
      
        labels = {
            'value' : 'Place you vote',
            'body' : 'Add a comment with your vote'
        }
        
    
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)  # Tell it which class (css class!) we're modifying
        
        # loop over the form and add the css class 'input' to every field
        # loop through every single field and add a css class of 'input'
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})