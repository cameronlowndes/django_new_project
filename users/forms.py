from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User  # Correctly references the User model
        fields = ['username', 'email', 'password1', 'password2']  # Ensure fields are listed correctly