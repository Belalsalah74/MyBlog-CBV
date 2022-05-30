from .models import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

User = get_user_model()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']