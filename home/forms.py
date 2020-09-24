from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

class NewUserForm(forms.Form):
    firstname = forms.CharField(label='First', max_length=100)
    lastname = forms.CharField(label='Last', max_length=100)
    email = forms.CharField(label='Email', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    repeatpassword = forms.CharField(widget=forms.PasswordInput())
