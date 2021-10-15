from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def signin(request):
    return HttpResponse('Sign in')

def signup(request):
    return HttpResponse('Sign up')

def home(request):
    return render(request, 'app/home.html')