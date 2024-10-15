# blog/models.py 
# Define the data objects for our application 

from django.db import models

# Create your models here.

class Article(models.Model): 
    ''''Encapsulate the idea of one Article by some author.'''

    # data attributes of an Article:
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)

    def __str__(self) -> str:
        '''Return a string representation of this object.'''

        return f'{self.title} by {self.author}'
    
    def get_comments(self):
        '''Return a QuerySet of all comments on this Article'''

        # use the ORM to retrieve Comments for which the FK is this Article 
        comments = Comment.objects.filter(article=self)
    
class Comment(models.Model):
    '''Encapsulates the idea of a comment on an Article'''

    # model the 1 to the many relationship with Article (foreign key)
    article = models.ForeignKey("Article", on_delete=models.CASCADE)

    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        '''return the string representation of this comment.'''
        return f'{self.text}'


