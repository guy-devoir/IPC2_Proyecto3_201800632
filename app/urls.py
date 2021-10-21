from django.contrib import admin
from django.urls import path
from .views import help_, home, upload, peticiones

urlpatterns = [
    path('', home, name= 'home'),
    path('upload', upload, name='upload'),
    path('help', help_, name='help'),
    path('peticiones', peticiones, name='peticiones') 
]
