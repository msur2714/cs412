# define the views for the blog app
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .forms import * #import the forms (e.g. CreateCommentForm)
from django.urls import reverse
from typing import Any
import random

# class-based view 
class ShowAllView(ListView):
    '''The view to show all articles'''

    model = Article #the model to display 
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # this is the context variable to use on the template

class RandomArticleView(DetailView):
    '''Display one Article selected at Random'''

    model = Article 
    template_name = "blog/article.html"
    context_object_name = "article"

    # AttributeError: Generic detail view RandomArticleView must be called with either 
    # one solution: implement get_object method

    def get_object(self): 
        '''Return one Article chosed at random'''

        # retrieve all of the articles 
        all_articles = Article.objects.all()

        # pick one at random 
        article = random.choice(all_articles)
        return article
    
class ArticleView(DetailView):
    '''Display one Article selected '''
    
    model = Article 
    template_name = "blog/article.html"
    context_object_name = "article"

class CreateCommentView(CreateView):
    '''A view to create a Comment on an Article.
       on GET: send back the form to display
       on POST: read/process the form, and save new Comment '''

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        # get the context data from the superclass 
        context = super().get_context_data(**kwargs)

        # find the Article identified by the PK from the URL pattern 
        article = Article.objects.get(pk=self.kwargs['pk'])

        # add the article referred to by the URL into this context 
        context['article'] = article
        return context

    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success.'''
        # return 'show_all' 
        # return reverse('show_all') #look up 

        # find the Article identified by the PK from the URL pattern 
        # article = Article.objects.get(pk=self.kwargs['pk'])
        # return reverse('article', kwargs={'pk': article.pk})
        return reverse('article', kwargs=self.kwargs)
    
    def form_valid(self, form): 
        '''This method is called after the form is validated, 
           before saving data to the database.'''
        
        print(f'CreateCommentView.form_valid(): form={form.cleaned_data}')
        print(f'CreateCommentView.form_valid(): self.kwargs={self.kwargs}')

        # find the Article identified by the PK from the URL pattern 
        article = Article.objects.get(pk=self.kwargs['pk'])

        # attach this Article to the instance of the Comment to set its FK 
        form.instance.article = article 

        # delegate work to superclass version of this method 
        return super().form_valid(form)
    
class CreateArticleView(CreateView): 
    '''A view class to create a new Article instance.'''

    form_class = CreateArticleForm
    template_name = 'blog/create_article_form.html'

    def form_valid(self, form):
        '''This method is called as part of the form processing.'''
        print(f'CreateArticleView.form_valid(): form.cleaned_data={form.cleaned_data}')
        return super().form_valid(form)
