from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm       # This is like a Model Form (built in django)
from .models import Profile



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name':'Name',
        }
        
        
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)  # Tell it which class (css class!) we're modifying
        
        # loop over the form and add the css class 'input' to every field
        # loop through every single field in the UserCreationForm and add a css class of 'input'
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
            
    

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username', 'location',
                  'bio', 'short_intro', 'profile_image',
                  'social_github','social_twitter', 'social_linkedin',
                  'social_youtube', 'social_website']