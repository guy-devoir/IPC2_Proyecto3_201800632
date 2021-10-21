from django.shortcuts import render, get_object_or_404, redirect 
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

# Create your views here.
def home(request):
    return render(request, 'app/home.html')

def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
    return render(request, 'app/upload.html')

def help_(request):
    return render(request, 'app/help.html')

def peticiones(request):
    return render(request, 'app/peticiones.html')