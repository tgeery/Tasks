from django.shortcuts import render
from .forms import LoginForm, NewUserForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request, *args, **kwargs):
    loginform = LoginForm()
    newuserform = NewUserForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print('loggin in or creating {} {}'.format(form.cleaned_data['username'], form.cleaned_data['password']))
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return render(request, 'index.html', {})
    return render(request, 'index.html', {'loginform': loginform, 'newuserform': newuserform})

def userlogout(request, *args, **kwargs):
    logout(request)
    loginform = LoginForm()
    newuserform = NewUserForm()
    return render(request, 'index.html', {'loginform': loginform, 'newuserform': newuserform})
