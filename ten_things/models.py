from django.db import models
from django.db.models import CharField, DateField
from datetime import datetime, date

# Create your models here.
class TenThingsModel(models.Model):
    date = models.DateTimeField(default=datetime.now, blank=True)
    theme = CharField(max_length=100)
    idea1 = CharField(max_length=100)
    idea2 = CharField(max_length=100)
    idea3 = CharField(max_length=100)
    idea4 = CharField(max_length=100)
    idea5 = CharField(max_length=100)
    idea6 = CharField(max_length=100)
    idea7 = CharField(max_length=100)
    idea8 = CharField(max_length=100)
    idea9 = CharField(max_length=100)
    idea10 = CharField(max_length=100)
