## voter_analytics/urls.py
## description: URL patterns for the voter_analytics app

from django.urls import path
from . import views 

urlpatterns = [
    # map the URL (empty string) to the view
    path('', views.VoterListView.as_view(), name='home'),
    # path('voter/', views.VoterDetailView.as_view(), name='voters'),
    path('voter/', views.VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>/', views.VoterDetailView.as_view(), name='voter'),
    path('graphs/', views.VoterGraphView.as_view(), name='graphs'),
]
