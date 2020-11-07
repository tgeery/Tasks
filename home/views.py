from django.shortcuts import render
from .forms import LoginForm, NewUserForm, TasksForm, CurrentTasksForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserTasks
from datetime import date


def index(request, *args, **kwargs):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                uid = int(request.user.id)
                tasks = CurrentTasksForm(userid=uid)
                return render(request, 'index.html', {'tasks':tasks})
    else:
        if request.user.is_authenticated:
            uid = int(request.user.id)
            tasks = CurrentTasksForm(userid=uid)
            return render(request, 'index.html', {"tasks":tasks})
        else:
            loginform = LoginForm()
            newuserform = NewUserForm()
    return render(request, 'index.html', {'loginform': loginform, 'newuserform': newuserform})

def userlogout(request, *args, **kwargs):
    logout(request)
    loginform = LoginForm()
    newuserform = NewUserForm()
    return render(request, 'index.html', {'loginform': loginform, 'newuserform': newuserform})

def userProfile(request, *args, **kwargs):
    if request.user.is_authenticated:
        uid = request.user.id
    if request.method == 'POST':
        tasksform = TasksForm(request.POST, user_key=uid)
    else:
        tasksform = TasksForm(user_key=uid)
    return render(request, 'profile.html', {'tasksform': tasksform, 'cnt': tasksform.cnt})
