from turtle import title
from django.db import models
from django.utils.timezone import datetime

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    