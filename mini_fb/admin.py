# mini_fb/admin.py
# Tell the admin that we want to administer these models

from django.contrib import admin

# Register your models here.

from .models import Profile
admin.site.register(Profile)