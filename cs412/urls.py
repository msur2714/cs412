"""
URL configuration for cs412 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static 
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hw/", include("hw.urls")), #create a URL hw/, and associate it with URLs in another file 
    path("quotes/", include("quotes.urls")), #create a URL quotes/, and associate it with URLs in another file
    path("formdata/", include("formdata.urls")), #create a URL formdata/, and associate it with URLs in another file
    path("restaurant/", include("restaurant.urls")), #create a URL restaurant/, and associate it with URLs in another file
    path("blog/", include("blog.urls")), #create a URL blog/, and associate it with URLs in another file
    path("mini_fb/", include("mini_fb.urls")), #create a URL mini_fb/, and associate it with URLs in another file
    path("marathon_analytics/", include("marathon_analytics.urls")), #create a URL marathon_analytics/, and associate it with URLs in another file
    path("voter_analytics/", include("voter_analytics.urls")), #create a URL voter_analytics/, and associate it with URLs in another file
] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)