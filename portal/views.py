from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request,'portal/index.html',{})

def events(request):
    return render(request,'portal/events.html',{})
def almanac(request):
    return render(request,'portal/almanac.html',{})
def timetable(request):
    return render(request,'portal/timetable.html',{})

