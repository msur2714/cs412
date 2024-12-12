from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static


# all of the URLs that are part of this app

urlpatterns = [
    path('', views.DashboardDetailView.as_view(), name="dashboard"),
    path('dashboard', views.DashboardDetailView.as_view(), name="dashboard"),
    
    # Review URLs - Create, Delete, Edit
    path('add', views.AddView.as_view(), name="add"),
    path('add_review', views.AddReviewView.as_view(), name="add_review"),
    path('review_add/<int:book_id>/', views.ReviewAddView.as_view(), name="review_add"),
    path('books/<int:book_id>/', views.ShowBookView.as_view(), name="show_book"),
    path('books/<int:book_id>/delete', views.DeleteBookView.as_view(), name="delete_book"),
    path('reviews/<int:pk>/edit/', views.EditReviewView.as_view(), name='edit_review'),
    path('review/<int:review_id>/delete/', views.DeleteReviewView.as_view(), name='delete_review'),

    # Reader Profile URLs
    path('showuser/<int:user_id>/', views.ReaderDetailView.as_view(), name='show_user'),
    path('edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),


    # Book Tracker URLs
    path('currently_reading/', views.CurrentlyReadingView.as_view(), name='currently_reading'),    
    path('book_history/', views.BookHistoryView.as_view(), name='book_history'),
    path('add_book/', views.BookCreateView.as_view(), name='add_book'),
    path('update_book/<int:pk>/', views.BookUpdateView.as_view(), name='update_book'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),  # Book Detail URL
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),

    # Authentication URLs
    path('login', views.LoginView.as_view(), name="login"),
    path('logout', views.LogoutView.as_view(), name="logout"),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'), ## NEW
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name='logout'), ## NEW
    path('register/', views.RegistrationView.as_view(), name='register')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
