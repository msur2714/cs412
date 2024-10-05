# define the views for the blog app
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import *

# class-based view 
class ShowAllView(ListView):
    '''The view to show all articles'''

    model = Article #the model to display 
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # this is the context variable to use on the template
