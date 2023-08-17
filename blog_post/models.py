from django.db import models
from django.contrib.auth import get_user_model

class BlogModel(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image=models.ImageField(upload_to='blog')
    upload_to=models.DateTimeField(auto_now=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes=models.ManyToManyField(get_user_model(),related_name='blog_posts')
    
    class Meta:
        permissions = [
            ("can_edit_or_delete_item", "Can_edit_own or can_delete_own"),
    ]



    def total_likes(self):
        return self.likes.count()

class comment(models.Model):
    post=models.ForeignKey(BlogModel,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    body=models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title,self.name)
