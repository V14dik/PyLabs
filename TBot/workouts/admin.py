from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from workouts.models import Workout
from workouts.models import Exercise
from workouts.models import WorkoutExercises


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
	list_display = ("name", "date", "time", "user")


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
	list_display = ("name", )


@admin.register(WorkoutExercises)
class WorkoutExercises(admin.ModelAdmin):
	list_display = ("workout", "exercises", "number",)