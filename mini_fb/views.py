# mini_fb/views.py
# define the views for the mini_fb app

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import *

class ShowAllView(ListView):
    '''The view to show all Profiles'''

    model = Profile 
    template_name = 'mini_fb/show_all.html'
    context_object_name = 'profiles' 
