from django import forms
from django.contrib.auth.models import User


class SignupForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.CharField(widget=forms.EmailInput)

    def clean_username(self):

        username = self.cleaned_data.get('username')
        if username == "" or User.objects.filter(username=username).exists():
            return forms.ValidationError('Username cannot be empty or duplicate.')
        return username

    def clean_email(self):

        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            return forms.ValidationError('Email address cannot be duplicated.')
        return email

    def clean_password2(self):

        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        print(password2, password)

        if password != password2:
            return forms.ValidationError('Password must be match. Please enter correct password.')
        return password2


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
