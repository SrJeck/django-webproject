from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings

from jobPortalApp.models import *

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class resumeForm(forms.ModelForm):
    class Meta:
        model = RESUME
        fields = ('resume',)