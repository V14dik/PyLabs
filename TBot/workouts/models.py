from django.db import models
import datetime


class Workout(models.Model):
	name  = models.CharField(max_length = 20)
	date = models.DateField(default = datetime.date.today)
	time = models.TimeField(default = datetime.time(9, 00))


class Exercise(models.Model):
	name = models.CharField(max_length = 20)
	