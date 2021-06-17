from django.http import HttpResponse
import datetime
import json

from .models import Workout, Exercise, WorkoutExercises
from users.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def add_user(request):
    if request.method != 'POST':
        return HttpResponse()
    new_user = json.loads(str(request.body[0]))
    new_user_i = json.loads(str(request.body[1]))
    print(new_user)
    try:
        user, _ = User.objects.get_or_create(u_id = new_user_i)
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
    user = User.objects.get(u_id = workout_info.get('user'))
    workout = Workout.objects.create(name = workout_info.get('name'),
                                     date = workout_info.get('date'), 
                                     time = workout_info.get('time'), 
                                     user = user)
    
    for key, value in workout_exercises.items():
        exercise, _ = Exercise.objects.get_or_create(name = key)
        work_exer = WorkoutExercises.objects.create(workout = workout,
                                                    number = value,
                                                    exercises = exercise)
    
    #html = "<html><body>%s</body></html>" % workout.id
    return HttpResponse('Workout added!')


@csrf_exempt
def delete_workout(request):
    if request.method != 'DELET':
        return HttpResponse()
    print('+' + request.body + '+')


@csrf_exempt
def see_workouts(request):
    if request.method != 'GET':
        return HttpResponse()
    u_id = request.GET.get('u_id')
    #user_id=u_id
    workouts_arr = []
    workouts = Workout.objects.filter(user__u_id = u_id).all()
    for w in workouts:
        exercises = w.exercises.all()
        exercises_dict = []
        for e in exercises:
            workout_ex = WorkoutExercises.objects.filter(workout= w, exercises = e).first()
            exercises_dict.append({'name':e.name,'number':workout_ex.number})
        
        work = {'workout':{
        'name':w.name,
        'date':w.date,
        'time':w.time,
        'user':w.user.u_id
        }, 'exercises':exercises_dict}
        
        workouts_arr.append(work)
    return JsonResponse(workouts_arr, safe = False)
    #return HttpResponse(workouts)
