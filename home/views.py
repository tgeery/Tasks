from django.shortcuts import render
from .forms import LoginForm, NewUserForm

# Create your views here.
def index(request, *args, **kwargs):
    loginform = LoginForm()
    newuserform = NewUserForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print('{} {}'.format(form.cleaned_data['username'], form.cleaned_data['password']))
            return render(request, 'index.html', {})
    return render(request, 'index.html', {'loginform': loginform, 'newuserform': newuserform})
