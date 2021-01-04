from django.shortcuts import render
from home.models import UserTasks


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        uid = int(request.user.id)
        tasks = UserTasks(userid=uid)
        return render(request, 'schedule.html', {})