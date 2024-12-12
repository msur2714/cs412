from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse, HttpRequest,Http404
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView, ListView, FormView, DeleteView
from django.views import View
from .models import Reader, Book, Review, User, BookLog, Image
from .forms import CustomUserCreationForm, ReviewForm, BookForm, BookUpdateForm, BookLogForm, EditReviewForm, ReaderUpdateForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 
from typing import Any
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardDetailView(LoginRequiredMixin, DetailView):
    '''This View displays the home page of the Book App to the Reader. 
       It shows the various features, such as adding books and reviews, 
       and shows a list of all their book reviews.'''
    
    model = Reader
    template_name = 'project/dashboard.html'
    context_object_name = 'reader'

    def get_login_url(self) -> str:
        return reverse('login')

    def get_object(self, queryset=None):
        user = self.request.user
        reader, created = Reader.objects.get_or_create(user=user)
        return reader
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ensure that the user is a Reader instance
        try:
            reader = Reader.objects.get(user=self.request.user)
            # Fix the query to use the 'reader' field for filtering
            reviews = Review.objects.filter(user=reader)
            context['reviews'] = reviews
        except Reader.DoesNotExist:
            context['reviews'] = None
        return context

class ReaderDetailView(LoginRequiredMixin, DetailView):
    '''This View displays the Reader's profile page. 
    
       It display the Reader's first and last name, email
       and their profile picture.'''
    
    model = Reader
    template_name = 'project/showuser.html'
    context_object_name = 'reader'

    def get_object(self, queryset=None):
        user = self.request.user
        reader, created = Reader.objects.get_or_create(user=user)
        return reader
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ensure that the user is a Reader instance
        try:
            reader = Reader.objects.get(user=self.request.user)
            reviews = Review.objects.filter(user=reader)
            context['reviews'] = reviews
        except Reader.DoesNotExist:
            context['reviews'] = None
        return context

    def get_login_url(self) -> str:
        return reverse('login')
    
    def get_success_url(self):
        return reverse('show_user', kwargs={'id': self.object.id})

class EditReaderView(LoginRequiredMixin, UpdateView):
    '''This allows a Reader to edit their profile page.'''

    model = Reader
    form_class = ReaderUpdateForm
    template_name = 'project/edit_reader.html'

    def get_object(self):
        return self.request.user.reader  

    def form_valid(self, form):
        self.object = form.save()

        return redirect('show_user', user_id=self.object.user.id) 

class RegistrationView(CreateView):
    '''This View handles registration of new users.'''

    template_name = 'project/register.html'
    form_class = CustomUserCreationForm 
    model = Reader 

    def dispatch(self, request, *args, **kwargs):
        '''Handle the User creation form submission'''

        if self.request.POST:
            # Handle POST requests
            print(f"RegistrationView.dispatch: self.request.POST={self.request.POST}")

            # Reconstruct the form from POST data
            form = self.form_class(self.request.POST)

            if not form.is_valid():
                print(f"form.errors = {form.errors}")
                return super().dispatch(request, *args, **kwargs)

            # Save the form, creating a new User
            user = form.save()
            print(f"RegistrationView.dispatch: created user {user}")

            # Log the User in
            login(self.request, user)
            print(f"RegistrationView.dispatch: {user} is logged in")

            # Redirect to a different page
            return redirect(reverse('show_user', args=[user.id]))

        # Let CreateView.dispatch handle HTTP GET requests
        return super().dispatch(request, *args, **kwargs)
    
class LoginView(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  
            request.session['user_id'] = user.id 
            return redirect('dashboard')
        else:
            # Handle invalid credentials
            return render(request, 'project/login.html', {'error': 'Invalid username or password'})

class BookHistoryView(ListView):
    '''This View displays all the books in a Reader's reading history. 
       So all book, whether they are being currently read or is read'''
    
    model = Book
    template_name = 'project/book_history.html'
    context_object_name = 'book_history'

    def get_queryset(self):
        query = self.request.GET.get('q')
        
        # Get the Reader instance corresponding to the authenticated user
        reader = get_object_or_404(Reader, user=self.request.user)

        # Start by filtering books based on the current user and their read status
        queryset = Book.objects.filter(
            reader=reader
        )

        # Additional filtering for books that are either read or currently being read
        queryset = queryset.filter(
            Q(is_read=True) | Q(is_currently_reading=True)
        )
        
        # If there's a query parameter, filter by title or author
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(author__icontains=query)
            )
        
        return queryset

# Book Views 
class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'project/book_form.html'
    success_url = reverse_lazy('currently_reading')


    def form_valid(self, form):
        # Fetch the Reader instance associated with the logged-in user
        try:
            reader = Reader.objects.get(user=self.request.user)
        except Reader.DoesNotExist:
            # Handle the case where a Reader instance is not created for the User
            return self.form_invalid(form)
        
        # Assign the Reader instance to the form
        form.instance.reader = reader
        return super().form_valid(form)

class BookUpdateView(UpdateView):
    model = Book
    form_class = BookUpdateForm
    template_name = 'project/book_update_form.html'
    success_url = reverse_lazy('currently_reading')

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)

class BookDetailView(DetailView):
    model = Book
    template_name = 'project/book_detail.html'
    context_object_name = 'book'

class DeleteBookView(DeleteView):
    '''This view is used to delete a book'''
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        book.delete()
        return redirect('dashboard')

class CurrentlyReadingView(LoginRequiredMixin, TemplateView, FormView):
    template_name = 'project/currently_reading.html'
    form_class = BookLogForm
    context_object_name = "currently_reading"
    success_url = reverse_lazy('currently_reading')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Use the Reader instance
        reader = self.request.user.reader
        
        currently_reading_books = Book.objects.filter(reader=reader, is_currently_reading=True)
        all_books = Book.objects.filter(reader=reader)

        # Prepare data for the chart
        labels = [book.title for book in all_books]
        data = []
        for book in all_books:
            book_log = BookLog.objects.filter(book=book).first()
            if book_log and book_log.total_pages > 0:
                progress = (book_log.current_page / book_log.total_pages) * 100
            else:
                progress = 0
            data.append(progress)

        context.update({
            'currently_reading_books': currently_reading_books,
            'all_books': all_books,
            'labels': labels,
            'data': data,
        })
        return context

    def form_valid(self, form):
        book_log = form.save(commit=False)
        book_log.user = self.request.user
        book_log.save()
        return super().form_valid(form)

@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    book.delete()
    return redirect('currently_reading')

# Views for Book Review
class CreateReviewView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'project/add_review.html'

    def get_form_kwargs(self):
        # Pass the current user to the form so we can filter the books correctly
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user.reader  # Ensure you're passing the reader instance
        return kwargs

    def form_valid(self, form):
        # Ensure the review is linked to the logged-in user and the selected book
        form.instance.user = self.request.user.reader
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the dashboard after successfully creating a review
        return reverse_lazy('dashboard')
    
class EditReviewView(UpdateView):
    '''This View allows a Reader to edit a Review that they have previously made'''
    model = Review
    form_class = EditReviewForm
    template_name = 'project/edit_review.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user.reader
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user.reader
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard') 

class DeleteReviewView(DeleteView):
    '''This View allows Readers to delete a review'''
    model = Review
    template_name = 'project/delete_review.html'
    success_url = reverse_lazy('dashboard') 

    def get_queryset(self):
        """Ensure that users can only delete their own reviews."""
        return Review.objects.filter(user=self.request.user.reader)
