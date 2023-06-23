from django.contrib.auth.forms import AuthenticationForm
from django import forms

from models import User

class UserLoginForm(AuthenticationForm):
    email = forms.CharField(widget=forms.EmailField(attrs={
        'placeholder': 'Введите ваш логин' 
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите ваш пароль' 
    }))
    
    class Meta:
        model = User
        fields = ('email', 'password')