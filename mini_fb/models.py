# mini_fb/models.py 
# Define the data objects for our application 

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model): 
    ''''Create profile for users which will model 
        the data attributes of individual Facebook users
        
        Data attributes: first name, last name, city, email 
                         address, and a profile image url.'''
    
    # Every Profile has one User:
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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
    
    def get_friends(self):
        '''Return all Friend relationships on each profile'''
        friends_as_profile1 = Friend.objects.filter(profile1=self)
        friends_as_profile2 = Friend.objects.filter(profile2=self)
        
        friends_profiles = [friend.profile2 for friend in friends_as_profile1] + [friend.profile1 for friend in friends_as_profile2]
        
        return friends_profiles
    
    def add_friend(self, other):
        if self == other:
            return  

        existing_friendship = Friend.objects.filter(
            models.Q(profile1=self, profile2=other) | 
            models.Q(profile1=other, profile2=self)
        ).exists()

        if not existing_friendship:
            Friend.objects.create(profile1=self, profile2=other)
    
    def get_friend_suggestions(self):
        # Retrieve all profiles that are not already friends and exclude the profile itself
        current_friends = set(self.get_friends())
        return Profile.objects.exclude(id__in=[friend.id for friend in current_friends]).exclude(id=self.id)

    def get_news_feed(self):
        # Get status messages for self
        self_statuses = StatusMessage.objects.filter(profile=self)
        
        # Get status messages for friends
        friends = self.get_friends()
        friends_statuses = StatusMessage.objects.filter(profile__in=friends)

        # Combine and order the messages by timestamp, most recent first
        all_statuses = (self_statuses | friends_statuses).order_by('-timestamp')
        return all_statuses
    
    
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

    def get_images(self):
        '''Return a QuerySet of all images related to this status message.'''
        return Image.objects.filter(status_message=self)
    
class Image(models.Model):
    ''''Create Image data model which encapsulates the idea 
        of an image file (not a URL) that is stored in the 
        Django media directory. which will model the data 
        
        Data attributes: image_file, status_message, timestamp'''
    
    image_file = models.ImageField(upload_to='images/') 
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    upload_timestamp = models.DateTimeField(auto_now=True)

class Friend(models.Model):
    '''Create Friends data model  which encapsulates the idea of 
       an edge connecting two nodes within the social network 
        
        Data attributes: profile1, profile2, timestamp'''
    
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.profile1} & {self.profile2}"
