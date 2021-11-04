from django.contrib import admin
from django.urls import path
from .views import help_, home, upload, peticiones, pdf_report

urlpatterns = [
    path('', home, name= 'home'),
    path('upload', upload, name='upload'),
    path('help', help_, name='help'),
    path('peticiones', peticiones, name='peticiones'), 
    path('reporte', pdf_report, name='reporte')
]
