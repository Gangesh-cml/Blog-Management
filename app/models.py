from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return self.user.username
    

class BlogModel(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    slug=models.SlugField(max_length=100)
    image=models.ImageField(upload_to='blog')
    created_at=models.DateTimeField(auto_now_add=True)
    upload_to=models.DateTimeField(auto_now=True)