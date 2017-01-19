from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from .models import *
from administration.models import *
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth import authenticate,login, logout
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from .forms import *

# Create your views here.

'''def index(request):
    all_notices = Notices.objects.all()
    content_notice = {
        'all_notices' : all_notices,
    }
    return render(request,'portal/index.html',content_notice)
'''

class index(TemplateView):
    template_name = 'portal/index.html'

    def get_context_data(self, **kwargs):
        context = super(index,self).get_context_data(**kwargs)
        context = {
            'all_notices' : Notices.objects.all()
        }
        return context

'''def events(request):
    all_events = Events.objects.all().order_by('-id')
    all_notices = Notices.objects.all()
    content_events = {

        'all_notices': all_notices,
        'all_events' : all_events
    }
    return render(request, 'portal/events.html', content_events)
'''

class events(TemplateView):
    template_name = 'portal/events.html'

    def get_context_data(self, **kwargs):
        context = super(events,self).get_context_data(**kwargs)
        context = {
            'all_notices' : Notices.objects.all(),
            'all_events' : Events.objects.all().order_by('-id')
        }
        return context


@login_required(redirect_field_name='message')
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



class requestForm(FormView):
    template_name = 'portal/requestform.html'
    form_class = formRequest

    def get(self, request):
        form = self.form_class(None)
        return render(request,self.template_name,{ 'form' : form})








class register(FormView):
    template_name = 'portal/register.html'
    form_class = registerForm
    def get(self, request, *args, **kwargs):
        form = self.form_class(None)
        context = {
            'form':form,
            'course_details':Course.objects.all(),
            'all_notices':Notices.objects.all()
        }
        return render(request,self.template_name,context)
 x

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


def forum(request):
    if  request.method == 'GET':
        all_threads = Forum.objects.all()
        content_thread = {
            'all_threads' : all_threads
        }
        return render(request,'portal/forum.html',content_thread)
    if request.method == 'POST':
        forum_new = Forum(
            thread_title = request.POST['title'],
            thread_description = request.POST['description'],
            thread_tag= request.POST['tags'],
            thread_user= request.user.get_full_name()
        )
        forum_new.save()
        return HttpResponseRedirect('/forum')


class credits(TemplateView):
    template_name = 'portal/credits.html'
    def get_context_data(self, **kwargs):
        context = super(credits,self).get_context_data(**kwargs)
        context = {
            'credits': Credits.objects.all()
        }
        return context