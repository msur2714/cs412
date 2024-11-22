from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import render
from .models import Book, ReadingEntry, Review
import random

# List of all books
class BookListView(ListView):

    model = Book 
    template_name = 'project/book_list.html'
    context_object_name = 'books' # how to find the data in the template file

# Book details
class BookDetailView(DetailView):

    model = Book 
    template_name = 'project/book_detail.html'
    context_object_name = 'book'

    def get_object(self): 
        '''Return one Book chosed at random'''

        # retrieve all of the articles 
        all_books = Book.objects.all()

        # pick one at random 
        book = random.choice(all_books)
        return book