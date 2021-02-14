from django.shortcuts import render
from .forms import LoginForm, FailedLoginForm, NewUserForm, TasksForm, CurrentTasksForm, TaskHistory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import UserTasks, CompletedTasks
from datetime import date


def is_authenticated(req):
    return True if req.user.is_authenticated else False

def is_post(req):
    return True if req.method == 'POST' else False

def get_userid(req):
    return int(req.user.id)

class GetHandle:
    newuserform = None
    def route(self, req):
        isAuth = is_authenticated(req)
        if isAuth:
            uid = int(req.user.id)
            tasks = CurrentTasksForm(userid=uid)
            return render(req, 'index.html', {"tasks":tasks})
        else:
            loginform = LoginForm()
            newuserform = NewUserForm()
        return render(req, 'index.html', {'loginform': loginform, 'newuserform': newuserform})

class PostHandle:
    def route(self, req):
        isAuth = is_authenticated(req)
        if isAuth:
            uid = get_userid(req)
            tasks = CurrentTasksForm(req.POST, userid=uid)
            return HttpResponseRedirect('/')
        else:
            loginform = LoginForm(req.POST)
            if loginform.is_valid():
                user = authenticate(req, username=loginform.cleaned_data['username'], password=loginform.cleaned_data['password'])
                if user is not None:
                    login(req, user)
                    uid = get_userid(req)
                    tasks = CurrentTasksForm(userid=uid)
                    return render(req, 'index.html', {'tasks':tasks})
                else:
                    loginform = FailedLoginForm()
        return render(req, 'index.html', {'loginform': loginform})

class RequestHandle:
    def route(self, req):
        isPost = is_post(req)
        if isPost:
            return PostHandle().route(req)
        else:
            return GetHandle().route(req)

def index(request, *args, **kwargs):
    return RequestHandle().route(request)

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
        data = []
        for task in taskhist:
            name = task.value().split(',')[0]
            dates = task.value().split(',')[1:]
            dates_str = ''
            for dt in dates:
                dates_str += dt + ','
            dates_str = dates_str.rstrip(',')
            data.append({'name':name, 'dates_lst':dates_str})
    return render(request, 'graphs.html', {'data': data})
