from django.shortcuts import render
from .models import TenThingsModel
from .forms import TenThings
from django.http import HttpResponseRedirect

# Create your views here.
def index(request, *args, **kwargs):
    if request.method == 'POST':
        if request.user.is_authenticated:
            t = TenThingsModel(theme=request.POST.get('theme',''),
                               idea1=request.POST.get('idea1',''),
                               idea2=request.POST.get('idea2',''),
                               idea3=request.POST.get('idea3',''),
                               idea4=request.POST.get('idea4',''),
                               idea5=request.POST.get('idea5',''),
                               idea6=request.POST.get('idea6',''),
                               idea7=request.POST.get('idea7',''),
                               idea8=request.POST.get('idea8',''),
                               idea9=request.POST.get('idea9',''),
                               idea10=request.POST.get('idea10',''))
            t.save()
            return HttpResponseRedirect('/')
    tenthingsform = TenThings()
    return render(request, 'ten_things_form.html', {'tenform': tenthingsform})
