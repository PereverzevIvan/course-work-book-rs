from django.contrib.auth.forms import AuthenticationForm
from django import forms

from .models import User

class UserLoginForm(AuthenticationForm):
    email = forms.EmailField(required=True ,widget=forms.EmailInput(attrs={
        'placeholder': 'Введите вашу почту',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите ваш пароль',
    }))
    
    class Meta:
        model = User
        fields = ('email', 'password')