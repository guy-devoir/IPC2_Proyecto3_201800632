from django.shortcuts import render, get_object_or_404, redirect 
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import requests
import os
import webbrowser

URL = 'http://localhost:4000/api'

# Create your views here.
def home(request):
    return render(request, 'app/home.html')

def pdf_report(request):
    webbrowser.open('file:///C:/Users/Luciano%20Xiqu%C3%ADn/Documents/Py-projects/IPC2_Proyecto3_201800632/frontend/app/documentacion.pdf')
    return render(request, 'app/help.html')

def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
    return render(request, 'app/upload.html')

def analize(request):
    data = {
        'archivo':{
            'content':""
        },
        'action' : ''
    }
    return render(request, 'app/home.html')

def help_(request):
    return render(request, 'app/help.html')

def peticiones(request):
    return render(request, 'app/peticiones.html')