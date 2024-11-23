from django import forms
from .models import Book, ReadingEntry, Review

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'publication_date', 'isbn', 'description']


class ReadingEntryForm(forms.ModelForm):
    class Meta:
        model = ReadingEntry
        fields = ['book', 'start_date', 'end_date', 'status', 'progress']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['book', 'rating', 'content']
