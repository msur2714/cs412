from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse, HttpRequest,Http404
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView, ListView, FormView
from django.views import View
from .models import Reader, Book, Review, User, BookLog, Image
from .forms import CustomUserCreationForm, ReviewForm, BookForm, BookUpdateForm, BookLogForm, ImageUploadForm, ReaderUpdateForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 
from typing import Any

# Authentication 
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardDetailView(LoginRequiredMixin, DetailView):
    model = Reader
    template_name = 'project/dashboard.html'
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


class ReaderDetailView(LoginRequiredMixin, DetailView):
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

class RegistrationView(CreateView):
    '''Handle registration of new users.'''

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
        
# Class-based add view
class AddView(View):
    def get(self, request):
        return render(request, 'project/add.html')

class AddReviewView(LoginRequiredMixin, View):
    model = Review
    template_name = 'project/add.html'
    form_class = ReviewForm

    def get_login_url(self) -> str:
        return reverse('login')
    
    def get_queryset(self): 
        reader = Reader.objects.get(user=self.request.user)
        book = BookLog.objects.get(user=self.request.user)
        queryset = Review.objects.filter(reader=reader).order_by('-date_logged')
        return queryset 
    
    def post(self, request):
        book = Book.objects.create(
            title=request.POST.get('title'),
            author=request.POST.get('author'),
            user=request.user,
        )

        Review.objects.create(
            user=request.user,
            book=book,
            review=request.POST.get('review'),
            rating=request.POST.get('rating'),
        )

        return redirect('dashboard')
    
    def add_review(request):
        query = request.GET.get('q')
        
        if query:
            books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))

        if request.method == 'POST':
            form = ReviewForm(request.POST, user=request.user)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user.reader  # Assuming each User has one Reader
                review.save()
                return redirect('book_history')  # Redirect to a relevant page after submission
        else:
            form = ReviewForm(user=request.user)

        context = {
            'form': form,
            'books': books,
            'query': query,
        }
        return render(request, 'project/add_review.html', context)

#show book view
class ShowBookView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        reviews = Review.objects.filter(book=book)
        context = {
            'book': book,
            'reviews': reviews
        }
        return render(request, 'project/show.html', context)

#review add view
class ReviewAddView(View):
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        review = Review(
            rating=request.POST.get('rating'),
            review=request.POST.get('review'),
            user=User.objects.get(id=request.session['user_id']),
            book=book
        )
        review.save()
        return redirect('dashboard')

class DeleteBookView(View):
    '''This view is used to delete a book'''
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        book.delete()
        return redirect('dashboard')

class DeleteReviewView(View):
    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)

        if review.user == request.user:
            review.delete()
            messages.success(request, "Review deleted successfully!")
        else:
            messages.error(request, "You cannot delete this review.")

        return redirect('dashboard')  

class LogoutView(View):
    def get(self, request):
        del request.session['user_id']
        return redirect('/')

class EditReviewView(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'project/edit_review.html'
    # Redirect to the dashboard after successful update
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        review = super().get_object(queryset)
        if review.user != self.request.user:
            # If the review does not belong to the logged-in user, redirect to dashboard
            raise PermissionDenied 
        return review

class BookHistoryView(ListView):
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
    
class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'project/book_form.html'
    success_url = reverse_lazy('currently_reading')

    def form_valid(self, form):
        form.instance.user = self.request.user
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

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Reader
    form_class = ReaderUpdateForm
    template_name = 'project/edit_reader.html'

    def get_object(self):
        # Ensure you are returning the correct Reader instance for the logged-in user
        return self.request.user.reader  # Assuming the user has a related Reader

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = ImageUploadForm(instance=self.object)  # For profile image upload
        return context

    def form_valid(self, form):
        # Save the Reader form data
        self.object = form.save()

        # Handle image form separately if an image is uploaded
        image_form = ImageUploadForm(self.request.POST, self.request.FILES, instance=self.object)
        if image_form.is_valid():
            image_form.save()  # Save the image

        return redirect('show_user', user_id=self.object.user.id)  # Redirect to profile page