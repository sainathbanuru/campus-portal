from django.shortcuts import render
from django.http import HttpResponse
from .models import Notices
# Create your views here.

def index(request):
    notices = Notices.objects.all()
    content_notice = {
        'notices' : notices,
    }
    return render(request,'portal/index.html',content_notice)

def events(request):
    return render(request,'portal/events.html',{})

def almanac(request):
    return render(request,'portal/almanac.html',{})

def timetable(request):
    return render(request,'portal/timetable.html',{})

def requestForm(request):
    return render(request,'portal/requestform.html',{})

def contact(request):
    return render(request,'portal/contact.html',{})
