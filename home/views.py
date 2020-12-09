from django.shortcuts import render
from .forms import LoginForm, FailedLoginForm, NewUserForm, TasksForm, CurrentTasksForm, TaskHistory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import UserTasks
from datetime import date


def index(request, *args, **kwargs):
    newuserform = None
    if request.method == 'POST':
        if request.user.is_authenticated:
            uid = int(request.user.id)
            CurrentTasksForm(request.POST, userid=uid)
            return HttpResponseRedirect('/')
        else:
            loginform = LoginForm(request.POST)
            if loginform.is_valid():
                user = authenticate(request, username=loginform.cleaned_data['username'], password=loginform.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    uid = int(request.user.id)
                    tasks = CurrentTasksForm(userid=uid)
                    return render(request, 'index.html', {'tasks':tasks})
                else:
                    loginform = FailedLoginForm()
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

def userGraphs(request, *args, **kwargs):
    if request.user.is_authenticated:
        uid = int(request.user.id)
        taskhist = TaskHistory(userid=uid)
    return render(request, 'graphs.html', {'taskhistory': taskhist})
