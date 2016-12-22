from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from .models import Notices,Events
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth import authenticate,login, logout


# Create your views here.

def index(request):
    all_notices = Notices.objects.all()
    content_notice = {
        'all_notices' : all_notices,
    }
    return render(request,'portal/index.html',content_notice)

def events(request):
    all_events = Events.objects.all().order_by('-id')
    all_notices = Notices.objects.all()
    content_events = {

        'all_notices': all_notices,
        'all_events' : all_events
    }
    return render(request, 'portal/events.html', content_events)
@login_required
def almanac(request):
    all_notices = Notices.objects.all()
    content_notice = {
        'all_notices': all_notices,
    }
    return render(request,'portal/almanac.html',content_notice)

def timetable(request):
    all_notices = Notices.objects.all()
    content_notice = {
        'all_notices': all_notices,
    }
    return render(request,'portal/timetable.html',content_notice)

def requestForm(request):
    all_notices = Notices.objects.all()
    content_notice = {
        'all_notices': all_notices,
    }
    return render(request,'portal/requestform.html',content_notice)

def contact(request):
    all_notices = Notices.objects.all()
    content_notice = {
        'all_notices': all_notices,
    }
    return render(request,'portal/contact.html',content_notice)

@login_required
def addEvent(request):
    event = Events(
        event_title=request.POST['title'],
        event_date=request.POST['date'],
        event_duration=request.POST['duration'],
        event_description=request.POST['description'],
        event_contact=request.POST['contact'],
        event_user=request.user.get_full_name()
    )
    event.save()
    return HttpResponseRedirect('/events')

def login_user(request):
    if request.method == 'GET':
        return render(request,'portal/login.html',{})
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['pass']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/')
            else:
                return render(request, 'portal/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'portal/login.html', {'error_message': 'Invalid login'})
    return render(request, 'portal/login.html')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def changepassword(request):
    if request.method =='GET':
        all_notices = Notices.objects.all()
        content_notice = {
            'all_notices': all_notices,
        }
        return render(request,'portal/changepassword.html',content_notice)
    if request.method == 'POST':
        request.user.first_name = request.POST['name']
        request.user.email = request.POST['email']
        if request.POST['password'] == request.POST['rpassword']:
            request.user.set_password(request.POST['password'])
        else:
            return render(request,'portal/changepassword.html',{'error_message' :'Password doesnot match'})
        request.user.save()
        return HttpResponseRedirect('/')





















