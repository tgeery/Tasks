from django import forms
from .models import UserTasks, CompletedTasks
from datetime import date


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())


class FailedLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    errMsg = forms.CharField(label='', initial='Invalid credentials', widget=forms.TextInput(attrs={'readonly':'readonly','style':'border: none;'}))


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
        if len(args) > 0:
            name = ''
            for arg in args[0]:
                if 'name' in arg:
                    name = args[0][arg]
            if len(name) > 0:
                t = tasks.filter(linkname=name)
                dt = date.today()
                if not (dt.year == t[0].lastdate.year and dt.month == t[0].lastdate.month and dt.day == t[0].lastdate.day):
                    n = CompletedTasks.objects.all().count()
                    h = CompletedTasks(n+1, t[0].userid, t[0].linkname, t[0].linkurl, date(dt.year, dt.month, dt.day))
                    h.save()
                    u = UserTasks(t[0].uid, t[0].userid, t[0].linkname, t[0].linkurl, date(dt.year, dt.month, dt.day))
                    u.save(update_fields=['lastdate'])
        else:
            for task in tasks:
                st = 'Complete' if date.today().year == task.lastdate.year and date.today().month == task.lastdate.month and date.today().day == task.lastdate.day else 'Incomplete'
                st_clr = 'lightgreen' if st == 'Complete' else 'lightcoral'
                self.fields['status{}'.format(self.cnt)] = forms.CharField(initial=st, max_length=50, widget=forms.TextInput(attrs={'readonly':'readonly','style':'border: none; width: 100px; background-color: {}; padding-left: 10px; padding-right: 10px;'.format(st_clr)}))
                self.fields['name{}'.format(self.cnt)] = forms.CharField(initial=task.linkname, max_length=100, widget=forms.TextInput(attrs={'readonly':'readonly','style':'border: none;'}))
                self.fields['url{}'.format(self.cnt)] = forms.CharField(initial=task.linkurl, max_length=200, widget=forms.TextInput(attrs={'readonly':'readonly','style':'border: none;'}))
                dt = task.lastdate.strftime("%B %d, %Y")
                self.fields['date{}'.format(self.cnt)] = forms.CharField(initial=dt, max_length=100, widget=forms.TextInput(attrs={'readonly':'readonly','style':'border: none;'}))
                self.cnt += 1
    
    def getCount():
        return self.cnt


class TaskHistory(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TaskHistory, self).__init__(*args)
        self.taskcnt = 0
        self.cnt = 0
        uid = kwargs['userid']
        tasks = UserTasks.objects.filter(userid=uid)
        for task in tasks:
            s = '{}'.format(task.linkname)
            #self.fields['sec{}'.format(self.taskcnt)] = forms.CharField(initial=task.linkname, label='', max_length=100, widget=forms.TextInput(attrs={'readonly':'readonly','style':'border: none;'}))
            hist = CompletedTasks.objects.filter(userid=uid,linkname=task.linkname,linkurl=task.linkurl)
            for h in hist:
                #self.fields['date{}'.format(self.cnt)] = forms.CharField(initial=h.completedate, label='', max_length=100, widget=forms.TextInput(attrs={'readonly':'readonly','style':'border: none;'}))
                s += ',{}'.format(h.completedate)
                self.cnt += 1
            self.fields['list{}'.format(self.taskcnt)] = forms.CharField(initial=s, label='', max_length=100, widget=forms.TextInput(attrs={'readonly':'readonly','style':'border: none;'}))
            self.taskcnt += 1
