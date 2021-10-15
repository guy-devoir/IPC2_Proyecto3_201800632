from django.contrib import admin
from django.urls import path
from .views import signin, home, signup

urlpatterns = [
    path('', home, name= 'home'),
    path('signin', signin, name='signin'),
    path('signup', signup, name ='signup')
]