from django.shortcuts import render
from django.http import HttpResponse

# This file accepts HTTP requests and responds to them

# Create your views here.
def home(request):
    return render(request, 'homepage.html' )