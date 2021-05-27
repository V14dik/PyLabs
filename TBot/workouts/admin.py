from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from workouts.models import Workout
from workouts.models import Exercise


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
	list_display = ("name", "date", "time",)


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
	list_display = ("name", )