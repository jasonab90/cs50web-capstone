from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class Card(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=64)
	description = models.CharField(max_length=256)
	timestamp = models.DateTimeField(auto_now_add=True)
	favorite = models.BooleanField(default=False)
	hide_completed = models.BooleanField(default=False)
	archived = models.BooleanField(default=False)
	is_complete = models.BooleanField(default=False)

class Item(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	card = models.ForeignKey(Card, on_delete=models.CASCADE)
	text = models.CharField(max_length=256)
	description = models.CharField(max_length=256, default="")
	timestamp = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)

class Date(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	card = models.ForeignKey(Card, on_delete=models.CASCADE)
	date = models.DateField()