from django import forms
from .models import Profile

class SignupForm(forms.Form):
    image = forms.ImageField(label='Your Picture', required = False)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Fisrt Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    age = forms.IntegerField()
    unique_id = forms.CharField(required = False, label='Unique Id')
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter Password'}))

class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email Id'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))