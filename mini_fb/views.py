# mini_fb/views.py
# define the views for the mini_fb app

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .forms import * #import the forms (e.g. CreateProfileForm)
from typing import Any
from django.urls import reverse
from django.shortcuts import redirect

class ShowAllView(ListView):
    '''The view to show all Profiles'''

    model = Profile 
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' 

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile' 

class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def form_valid(self, form):
        profile = form.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})

class CreateStatusMessageView(CreateView):
    '''A view to create a Status Message on an Profile.
       on GET: send back the form to display 
       on POST: read/process the form, and save new Status Message'''
    
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''This method is called after the form is validated, 
           before saving data to the database.'''
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile 
        return super().form_valid(form)
    
    def get_success_url(self):
        '''Return the URL to redirect to on success.'''
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
