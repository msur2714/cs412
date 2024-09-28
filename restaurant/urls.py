## restaurant/urls.py
## description: URL patterns for the quotes app

from django.urls import path
from django.conf import settings
from . import views

# All of the URLs that are part of this app
# define a list of valid URL patterns: 

urlpatterns = [
    path('', views.main, name='main'),  # This will match /restaurant
    path('main/', views.main, name='main'),
    path('order/', views.order, name='order'),
    path('confirmation/', views.confirmation, name='confirmation'),
]