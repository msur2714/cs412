from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Reader(models.Model):
    """Create Reader for users to track their unique reading record."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.TextField(blank=False, max_length=20, null=True)
    last_name = models.TextField(blank=False, max_length=20, null=True)
    email_address = models.TextField(blank=False, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    """The Book model saves the books that a Reader has read."""
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField(default="No description available")
    is_read = models.BooleanField(default=False)
    is_currently_reading = models.BooleanField(default=False)
    user = models.ForeignKey(Reader, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} by {self.author}"


class BookLog(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    current_page = models.IntegerField(blank=False, default=0)
    total_pages = models.IntegerField(blank=False, default=0)

    def __str__(self):
        progress = (self.current_page / self.total_pages) * 100 if self.total_pages > 0 else 0
        return f"{self.book.title} - {progress:.2f}%"


class Review(models.Model):
    """The Review model stores the reviews a Reader makes on their books."""
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    review = models.TextField(blank=False, max_length=250, null=True)
    user = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(blank=False, null=True)

    def __str__(self):
        return f"Review of {self.book.title} by {self.user}"