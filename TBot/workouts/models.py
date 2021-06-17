from django.db import models
import datetime
from users.models import User


class Workout(models.Model):
	name  = models.CharField(max_length = 20)
	date = models.CharField(default = datetime.date.today,max_length = 10)
	time = models.CharField(default = datetime.time(9, 00), max_length = 5)
	#ForeignKey
	user = models.ForeignKey(User, on_delete = models.CASCADE)


class Exercise(models.Model):
	name = models.CharField(max_length = 20)
	workouts = models.ManyToManyField(Workout, through = "WorkoutExercises", related_name = 'exercises')
	

class WorkoutExercises(models.Model):
	workout = models.ForeignKey(Workout, on_delete = models.CASCADE)
	number = models.CharField(default = 15, max_length = 20)
	exercises = models.ForeignKey(Exercise, on_delete = models.CASCADE)
