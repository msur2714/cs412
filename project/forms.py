# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reader, Review, Book, BookLog

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    email = forms.EmailField(max_length=254, required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        # Save the User instance
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            # Create a corresponding Reader instance
            Reader.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email_address=user.email
            )
        return user
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['book', 'review', 'rating']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['book'].queryset = Book.objects.filter(
                user=user, is_read=True
            )

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'is_currently_reading', 'is_read']
    

class BookLogForm(forms.ModelForm):
    """Form for creating and updating BookLog entries."""

    class Meta:
        model = BookLog
        fields = ["book", "current_page", "total_pages"]
        widgets = {
            "book": forms.Select(attrs={
                "class": "form-control input-lg",
            }),
            "current_page": forms.NumberInput(attrs={
                "placeholder": "Current page",
                "class": "form-control input-lg",
            }),
            "total_pages": forms.NumberInput(attrs={
                "placeholder": "Total pages",
                "class": "form-control input-lg",
            }),
        }

    def save(self, commit=True):
        book_log = super().save(commit=False)
        # Additional processing if needed
        if commit:
            book_log.save()
        return book_log
    

class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['is_currently_reading', 'is_read']