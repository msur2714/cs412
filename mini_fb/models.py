# mini_fb/models.py 
# Define the data objects for our application 

from django.db import models

# Create your models here.

class Profile(models.Model): 
    ''''Create profile for users which will model 
        the data attributes of individual Facebook users
        
        Data attributes: first name, last name, city, email 
                         address, and a profile image url.'''

    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.TextField(blank=False)
    image_url = models.URLField(blank=True)

    def __str__(self) -> str:
        '''Return a string representation of this object.'''
        return f'{self.first_name} {self.last_name}'
    
    def get_status_messages(self):
        '''Return all of the Status Messages on this Profile.'''
        status_messages = StatusMessage.objects.filter(profile=self).order_by('-timestamp')
        return status_messages

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})  
    
    
class StatusMessage(models.Model): 
    ''''Create StatusMessage which will model the data 
        attributes of Facebook status message.
        
        Data attributes: timestamp, message, profile.'''

    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def __str__(self) -> str:
        '''Return a string representation of this object.'''
        return f'{self.message} posted on {self.timestamp}'


