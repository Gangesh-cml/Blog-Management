from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django import forms

from django import forms
from django.contrib.auth.models import Permission, User, Group

class AssignPermissionForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)
    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all())


