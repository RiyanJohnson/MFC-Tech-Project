from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
#from .models import chatbot

def home(request):
    return render(request, 'chatbot/landingpage.html')