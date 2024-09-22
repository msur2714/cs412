## quotes/urls.py
## description: URL patterns for the quotes app

from django.urls import path
from django.conf import settings
from . import views

# All of the URLs that are part of this app
urlpatterns = [
    path(r'', views.home, name="home"),
    path(r'about', views.about, name="about"),
    path(r'quote', views.quote, name="quote"),
    path(r'show_all', views.show_all, name="show_all"),
    
]