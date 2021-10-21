from django.contrib import admin
from django.urls import path
from .views import help_, home, todo_form, upload

urlpatterns = [
    path('', home, name= 'home'),
    path('todo_form',todo_form, name= 'todo_form'),
    path('upload', upload, name='upload'),
    path('help', help_, name='help')
]
