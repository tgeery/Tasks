from django.db import models
from django.db.models import CharField, IntegerField, UUIDField, DateField
from django_mysql.models import ListCharField
from datetime import date


class UserTasks(models.Model):
    uid = UUIDField(primary_key=True)
    userid = IntegerField()
    linkname = CharField(max_length=100)
    linkurl = CharField(max_length=100)
    lastdate = DateField()


class CompletedTasks(models.Model):
    uid = UUIDField(primary_key=True)
    userid = IntegerField()
    linkname = CharField(max_length=100)
    linkurl = CharField(max_length=100)
    completedate = DateField(default=date(1970,1,1))
