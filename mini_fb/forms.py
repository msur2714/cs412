# mini_fb/forms.py

from django import forms
from .models import Profile, StatusMessage

# class CreateProfileForm(forms.ModelForm):
#     '''A form to add/create a new Profile to the database'''

#     class Meta: 
#         '''Associate this HTML form with the StatusMessage data model'''

#         model = StatusMessage 
#         fields = ['message', 'profile']


class CreateProfileForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    email = forms.EmailField(label="Email", required=True)
    city = forms.CharField(label="City", required=True)
    image_url = forms.CharField(label="Image URL", required=True)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'city', 'image_url']  

class CreateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['message']  # Assuming 'message' is a field in your StatusMessage model
        labels = {'message': 'Status Message'}
