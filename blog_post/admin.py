from django.contrib import admin

# Register your models here.

from .models import BlogModel,comment

admin.site.register(BlogModel)
admin.site.register(comment)