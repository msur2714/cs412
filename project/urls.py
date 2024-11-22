## project/urls.py
## description: URL patterns for the bookmark app

from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

# all of the URLs that are part of this app
urlpatterns = [
    path(r'', views.BookListView.as_view(), name="book_list"),  
    path(r'book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
]
