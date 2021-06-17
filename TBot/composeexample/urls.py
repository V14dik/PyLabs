"""composeexample URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from workouts.views import add_workout, delete_workout, see_workouts, add_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_workout/', add_workout),
    path('delete_workout/', delete_workout),
    path('see_workouts/', see_workouts),
    path('add_user/', add_user),
]
