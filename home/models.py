from django.db import models
from django.db.models import CharField, IntegerField, UUIDField, DateField, TimeField, BooleanField
from django_mysql.models import ListCharField
from datetime import date, time


class UserTasks(models.Model):
    uid = UUIDField(primary_key=True)
    userid = IntegerField()
    linkname = CharField(max_length=100)
    linkurl = CharField(max_length=100)
    lastdate = DateField(default=date(1970,1,1))
    duration = IntegerField(default=15)
    share = BooleanField(default=False)


class CompletedTasks(models.Model):
    uid = UUIDField(primary_key=True)
    userid = IntegerField()
    linkname = CharField(max_length=1000)
    linkurl = CharField(max_length=1000)
    completedate = DateField(default=date(1970,1,1))
    duration = IntegerField(default=15)
