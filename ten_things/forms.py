from django import forms

# Create your models here.
class TenThings(forms.Form):
    theme = forms.CharField(max_length=100)
    idea1 = forms.CharField(max_length=100)
    idea2 = forms.CharField(max_length=100)
    idea3 = forms.CharField(max_length=100)
    idea4 = forms.CharField(max_length=100)
    idea5 = forms.CharField(max_length=100)
    idea6 = forms.CharField(max_length=100)
    idea7 = forms.CharField(max_length=100)
    idea8 = forms.CharField(max_length=100)
    idea9 = forms.CharField(max_length=100)
    idea10 = forms.CharField(max_length=100)
