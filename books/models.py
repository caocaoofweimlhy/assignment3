from django.db import models
from django.core.urlresolvers import reverse
from accounts.models import UserProfile

class Book(models.Model):
    user = models.ForeignKey(UserProfile, blank=True, null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    imageID = models.CharField(max_length=255)
    author = models.ForeignKey('Author', related_name= 'books', null=True, blank=True)
    genre = models.ManyToManyField('Genre', related_name='books', null=True, blank=True)
    date = models.DateField(auto_now_add=False, auto_now=False, null=True)
    
    def __unicode__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk":self.pk})
        
class Author(models.Model):
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title
        
class Genre(models.Model):
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title