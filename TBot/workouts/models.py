from django.db import models
import datetime
from users.models import User


class Workout(models.Model):
	name  = models.CharField(max_length = 20)
	date = models.DateField(default = datetime.date.today)
	time = models.TimeField(default = datetime.time(9, 00))
	user = models.ForeignKey(User, on_delete = models.CASCADE)


class Exercise(models.Model):
	name = models.CharField(max_length = 20)
	workouts = models.ManyToManyField(Workout, through = "WorkoutExercises")
	

class WorkoutExercises(models.Model):
	workout = models.OneToOneField(Workout, on_delete = models.CASCADE)
	number = models.IntegerField(default = 15)
	exercises = models.ForeignKey(Exercise, on_delete = models.CASCADE)
