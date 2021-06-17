from django.http import HttpResponse
import datetime
import json

from .models import Workout, Exercise, WorkoutExercises
from users.models import User
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def add_user(request):
    if request.method != 'POST':
        return HttpResponse()
    new_user = json.loads(str(request.body[0]))
    new_user_i = json.loads(str(request.body[1]))
    print(new_user)
    try:
        user = User.objects.create(u_id = new_user_i)
    except:
        pass
    return HttpResponse()


@csrf_exempt
def add_workout(request):
    #if not request.is_ajax():
        #return HttpResponse()
    if request.method != 'POST':
        return HttpResponse()
    #print(json.loads(request.body))
    new_workout = json.loads(request.body)
    print(new_workout)
    workout_info = new_workout.get('workout')
    workout_exercises = new_workout.get('exercises')
    print('====')
    user = User.objects.first()
    workout = Workout.objects.create(name = workout_info.get('name'),
                                     date = workout_info.get('date'), 
                                     time = workout_info.get('time'), 
                                     user = workout_info.get('user'))
    
    for key, value in workout_exercises.items():
        exercise = Exercise.objects.create(name = key)
        work_exer = WorkoutExercises.objects.create(workout = workout,
                                                    number = value,
                                                    exercises = exercise)
    
    #html = "<html><body>%s</body></html>" % workout.id
    return HttpResponse('Workout added!')


@csrf_exempt
def delete_workout(request):
    if request.method != 'GET':
        return HttpResponse()
    print('+' + request.body + '+')


@csrf_exempt
def see_workouts(request):
    if request.method != 'GET':
        return HttpResponse()
    u_id = str(json.loads(request.body))
    workouts = Workout.objects.filter(user = u_id).all()
    for i in workouts:
        print(i.name)
    return HttpResponse(workouts)
