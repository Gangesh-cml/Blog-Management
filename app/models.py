from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# Create your models here.



class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return self.user.username

# from django.contrib.auth.models import AbstractUser

# class CustomUser(AbstractUser):
#     USER_ROLES = (
#         ('admin', 'Admin'),
#         ('regular', 'Regular User'),
#     )
#     role = models.CharField(max_length=10, choices=USER_ROLES)


# from django.contrib.auth.models import Permission

# # Define permissions for admin role
# admin_permissions = [
#     Permission.objects.get(codename='add_post'),
#     Permission.objects.get(codename='change_post'),
#     Permission.objects.get(codename='delete_post'),
# ]

# # Define permissions for regular user role
# regular_permissions = [
#     Permission.objects.get(codename='add_post'),
#     Permission.objects.get(codename='change_own_post'),
#     Permission.objects.get(codename='delete_own_post'),
# ]
    
# from django.contrib.auth.models import Group

# admin_group, _ = Group.objects.get_or_create(name='Admin')
# regular_user_group, _ = Group.objects.get_or_create(name='Regular User')

# for permission in admin_permissions:
#     admin_group.permissions.add(permission)

# for permission in regular_permissions:
#     regular_user_group.permissions.add(permission)



