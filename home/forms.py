from django import forms
from .models import UserTasks
from datetime import date


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


class TasksForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TasksForm, self).__init__(*args)
        uid = kwargs['user_key']
        tasks = UserTasks.objects.filter(userid=uid)
        self.cnt = 0
        if len(args) > 0 and 'addItem' in args[0]:
            sz = int(args[0]['addItem']) + 1
        elif len(args) > 0 and 'removeItem' in args[0]:
            sz = int(args[0]['removeItem']) - 1
        elif len(args) > 0:
            name = ''
            sz = 0
            for item in args[0]:
                if 'name' in item:
                    name = args[0][item]
                elif 'url' in item:
                    url = args[0][item]
                    if len(tasks) > sz and tasks[sz].linkname != name and tasks[sz].linkurl != url:
                        u = UserTasks(sz+1, uid, name, url)
                        u.save(update_fields=['linkname','linkurl'])
                    else:
                        u = UserTasks(sz+1, uid, name, url)
                        u.save()
                    sz += 1
        else:
            sz = len(tasks)
        for i in range(0, sz):
            name_lbl = ''
            url_lbl = ''
            if len(tasks) > i:
                name_lbl = tasks[i].linkname
                url_lbl = tasks[i].linkurl
            self.fields['name{}'.format(self.cnt)] = forms.CharField(initial=name_lbl, label='', max_length=100)
            self.fields['url{}'.format(self.cnt)] = forms.CharField(initial=url_lbl, label='', max_length=100)
            self.cnt+=1
    
    def getCount():
        return self.cnt


class CurrentTasksForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CurrentTasksForm, self).__init__(*args)
        self.cnt = 0
        uid = kwargs['userid']
        tasks = UserTasks.objects.filter(userid=uid)
        for task in tasks:
            st = 'Complete' if date.today() == task.lastdate else 'Incomplete'
            self.fields['status{}'.format(self.cnt)] = forms.CharField(initial=st, max_length=50, widget=forms.TextInput(attrs={'readonly':'readonly','style':'border: none; width: 100px; background-color: lightcoral; padding-left: 10px; padding-right: 10px;'}))
            self.fields['name{}'.format(self.cnt)] = forms.CharField(initial=task.linkname, max_length=100, widget=forms.TextInput(attrs={'readonly':'readonly','style':'border: none;'}))
            self.fields['url{}'.format(self.cnt)] = forms.CharField(initial=task.linkurl, max_length=200, widget=forms.TextInput(attrs={'readonly':'readonly','style':'border: none;'}))
            self.fields['date{}'.format(self.cnt)] = forms.CharField(initial=task.lastdate, max_length=100, widget=forms.TextInput(attrs={'readonly':'readonly','style':'border: none;'}))
            self.cnt += 1
    
    def getCount():
        return self.cnt