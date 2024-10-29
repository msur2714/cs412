# mini_fb/views.py
# define the views for the mini_fb app

from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
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
        
        # Save the status message
        sm = form.save()

        # Handle file uploads (if any)
        files = self.request.FILES.getlist('files')  # Get list of uploaded files

        for file in files:
            # Create an Image object for each file
            image = Image(image_file=file, status_message=sm)
            image.save()

        return super().form_valid(form)
    
    def get_success_url(self):
        '''Return the URL to redirect to on success.'''
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
    
class UpdateProfileView(UpdateView):
    '''A view to update the Profile details.'''
    
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        '''Redirect back to the profile page after updating.'''
        return reverse('show_profile', kwargs={'pk': self.object.pk})

class DeleteStatusMessageView(DeleteView):
    '''A view to delete a StatusMessage.'''
    
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        '''Redirect to the profile page after a successful delete.'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
class UpdateStatusMessageView(UpdateView):
    '''A view to update a StatusMessage.'''

    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'

    def get_success_url(self):
        '''Redirect to the profile page after a successful update.'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class CreateFriendView(View):
    def dispatch(self, request, *args, **kwargs):
        profile_pk = kwargs.get('pk')
        other_profile_pk = kwargs.get('other_pk')

        try:
            profile = Profile.objects.get(pk=profile_pk)
            other_profile = Profile.objects.get(pk=other_profile_pk)

            profile.add_friend(other_profile)

            return redirect('profile_detail', pk=profile_pk)

        except Profile.DoesNotExist:
            return redirect('profile_list')  

class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['friend_suggestions'] = profile.get_friend_suggestions()
        return context

class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['news_feed'] = profile.get_news_feed()
        return context