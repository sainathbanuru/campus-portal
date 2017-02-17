from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail,BadHeaderError
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse

from portal.serializers import UserSerializer
from .models import *
from administration.models import *
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth import authenticate,login, logout
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from .forms import *
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
# Create your views here.

'''def index(request):
    all_notices = Notices.objects.all()
    content_notice = {
        'all_notices' : all_notices,
    }
    return render(request,'portal/index.html',content_notice)
'''
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


class index(TemplateView):
    template_name = 'portal/index.html'

    def get(self, request, *args, **kwargs):
        context = {
            'all_notices': Notices.objects.all(),
        }

        if request.user.groups.filter(name='student').exists():
            context = {
                'all_notices': Notices.objects.all(),
                'student': 'student'
            }

        if request.user.groups.filter(name='admin').exists():
            context = {
                'all_notices': Notices.objects.all(),
                'admin': 'admin'
            }
        return render(request, 'portal/index.html', context)

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
    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(name='student').exists():
            context = {
                'all_notices': Notices.objects.all(),
                'all_events': Events.objects.all().order_by('-id'),
                'student':'student'
            }

        if request.user.groups.filter(name='admin').exists():
            context = {
                'all_notices': Notices.objects.all(),
                'all_events': Events.objects.all().order_by('-id'),
                'admin': 'admin'
            }

        return render(request,self.template_name,context)


@login_required(redirect_field_name='message')
def almanac(request):
    if request.user.groups.filter(name='student').exists():
        context = {
            'all_notices': Notices.objects.all(),
            'student': 'student'
        }

    if request.user.groups.filter(name='admin').exists():
        context = {
            'all_notices': Notices.objects.all(),
            'admin': 'admin'
        }
    return render(request,'portal/almanac.html',context)

def timetable(request):
    if request.user.groups.filter(name='student').exists():
        context = {
            'all_notices': Notices.objects.all(),
            'student': 'student'
        }

    if request.user.groups.filter(name='admin').exists():
        context = {
            'all_notices': Notices.objects.all(),
            'admin': 'admin'
        }
    return render(request,'portal/timetable.html',context)

class requestForm(FormView):
    template_name = 'portal/requestform.html'
    form_class = RequestForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):

        name = request.POST['name']
        fathersName = request.POST['fathersName']
        formRequired = request.POST['formRequired']
        reason = request.POST['reason']

        if name and fathersName and formRequired and reason:

            # return HttpResponse(name+fathersName+formRequired+reason)
            formreq = formRequest(
                form_name=name,
                form_fathersName=fathersName,
                form_required=formRequired,
                form_reason=reason
            )
            formreq.save()

            try:
                send_mail("Form Request", name + " requires " + formRequired + " for" + reason, "sainath.b14@iiits.in",
                          ['sainath.b14@iiits.in'])
            except BadHeaderError:
                return HttpResponse("Error sending mail")
            return HttpResponseRedirect('/')



'''def formsend(request):
    if request.method == 'POST':
        name = request.POST['name']
        fathersName = request.POST['fathersName']
        formRequired = request.POST['formRequired']
        reason = request.POST['reason']
        if name and fathersName and formRequired and reason:
            try:
                send_mail("Form Request", name + " requires " + formRequired + " for" + reason, "sainath.b14@iiits.in",
                          ['sainath.b14@iiits.in'])
            except BadHeaderError:
                return HttpResponse("Error sending mail")
            return HttpResponseRedirect('/index')


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
'''


class register(FormView):
    def get(self, request, *args, **kwargs):
        userId = request.user.id
        #return HttpResponse(userId)
        # Current User
        User = Students.objects.get(user = userId)
        #return HttpResponse(User.year)
        Year_of_study = User.year
        Branch_of_study = User.branch
        #return HttpResponse(User.branch)
        Courses_for_offering = []

        my_courses_list = [i.Course.course_title for i in User.student_course_set.all()]
        courses_registered = [Course.objects.get(course_title=i) for i in my_courses_list]

        if Year_of_study == 1:
            Courses_for_offering = Course.objects.filter(coursefor_ug1=True)
        if Year_of_study == 2:
            Courses_for_offering = Course.objects.filter(coursefor_ug2=True)
        if Year_of_study == 3:
            Courses_for_offering = Course.objects.filter(coursefor_ug3=True)
            #return HttpResponse(Courses_for_offering)
        if Year_of_study == 4:
            Courses_for_offering = Course.objects.filter(coursefor_ug4=True)

        FC = []
        BC = []
        IT_el = []
        MS_el = []  # Maths + Science
        H_el = []  # Humanities Elective
        S_el = []  # Skills Elective

        for course in Courses_for_offering:
            #return HttpResponse(course)
            if Branch_of_study == "CSE":
                if course.course_cse == "flexi_core":

                    FC.append(course)
                if course.course_cse == "bc_cse":
                    BC.append(course)
                if course.course_cse == "it_lective":
                    IT_el.append(course)

            if Branch_of_study == "ECE":
                if course.course_ece == "flexi_core":
                    FC.append(course)
                if course.course_ece == "bc_ece":
                    BC.append(course)
                if course.course_ece == "it_lective":
                    IT_el.append(course)

            if course.course_cse == "ms_elective":
                MS_el.append(course)

            if course.course_cse == "humanities":
                H_el.append(course)

            if course.course_cse == "skills":
                S_el.append(course)

        template_name = 'portal/register.html'

        context = {

            'FC': FC,
            'BC': BC,
            'IT_el': IT_el,
            'MS_el': MS_el,
            'H_el': H_el,
            'S_el': S_el,

            'all_notices': Notices.objects.all(),
            'courses_registered': courses_registered
        }
        return render(request, template_name, context)


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
        if "?next" in request.POST:
            return HttpResponse(request.POST['next'])
        username = request.POST['email']
        password = request.POST['pass']
        #return HttpResponse(username+password)
        user = authenticate(username=username, password=password)
       # return HttpResponse(user)
        print(user)
        if user is not None:
            if user.is_active:
                if "next" in request.POST:
                    return HttpResponse(request.POST['next'])
                if user.groups.filter(name='student').exists():
                    login(request, user)
                    return render(request, 'portal/index.html', {'student':'student'})
                if user.groups.filter(name='admin').exists():
                    login(request, user)
                    return render(request, 'portal/index.html', {'admin': 'admin'})
            else:
                return render(request, 'portal/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'portal/login.html', {'error_message': 'Invalid login'})
    return render(request, 'portal/index.html')

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


class Signup(FormView):

    template_name = 'portal/sign_up.html'
    form_class = SignupForm

    def get(self, request, context={}, *args, **kwargs):
        form = self.form_class(None)
        if context == {}:
            context = {'form':form}
        else:
            context['form'] = form

        return render(request, self.template_name, context)

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():

            name = form.cleaned_data['name']
            student_fathersName = form.cleaned_data['fname']
            student_roll = form.cleaned_data['roll']
            student_email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            cpassword = form.cleaned_data['cpassword']

            # Passwords are not coming correctly !!!!!!!!
            if password != cpassword:
                return render(request,'portal/sign_up.html',{'form':form,'error_message':'passwords didnot match'})

            student_phone = form.cleaned_data['phone']
            student_branch = form.cleaned_data['branch']
            student_year = form.cleaned_data['year']

  #          return HttpResponse('done')

            user = User.objects.create_user(
                username=student_email,
                first_name=name,
                email=student_email
            )
            user.set_password(password)
            user.is_active = True
            user.groups = [Group.objects.get(name='student')]
            user.save()

            student = Students.objects.create(
                user = user,
                fathers_name = student_fathersName,
                roll_no = student_roll,
                email=student_email,
                phone = student_phone,
                branch = student_branch,
                year = student_year
            )
            student.save()

#            return render(request, 'portal/sign_up.html', {'form': form, "pass1": password, "pass2": cpassword})
            return HttpResponseRedirect('/login')

 #       return render(request, 'portal/sign_up.html', {'form': form, "err": "some error"})



class unregister(FormView):
    def get(self, request, *args, **kwargs):
        current_student = Students.objects.get(user= request.user.id)
        my_courses_list = [i.Course.course_title for i in current_student.student_course_set.all()]
        courses_registered = [Course.objects.get(course_title=i) for i in my_courses_list]

        context = {'courses_registered': courses_registered}
        return render(request, 'portal/unregister.html', context)


# Runs in background
def unregister2(request):
    courses_selected = Course.objects.filter(id__in=request.POST.getlist('checks[]'))
    current_student = Students.objects.get(user= request.user.id)

    for course in courses_selected:
        Student_Course.objects.filter(Student=current_student).get(Course=course).delete()

    my_courses_list = [i.Course.course_title for i in current_student.student_course_set.all()]
    courses_registered = [Course.objects.get(course_title=i) for i in my_courses_list]

    context = {'courses_registered': courses_registered, 'branch': current_student.branch}
    return render(request, 'portal/my_courses.html', context)


def register_course(request):
    courses_selected = Course.objects.filter(id__in=request.POST.getlist('checks[]'))
    current_student = Students.objects.get(user= request.user.id)

    my_courses_list = [i.Course.course_title for i in current_student.student_course_set.all()]
    courses_registered = [Course.objects.get(course_title=i) for i in my_courses_list]

    # If not exists ...
    for current_course in courses_selected:
        if current_course not in courses_registered:
            s_c = Student_Course()
            s_c.Student = current_student
            s_c.Course = current_course
            s_c.save()

    current_student = Students.objects.get(user= request.user.id)
    my_courses_list = [i.Course.course_title for i in current_student.student_course_set.all()]
    courses_registered = [Course.objects.get(course_title=i) for i in my_courses_list]

    context = {'courses_registered': courses_registered, 'branch': current_student.branch}
    return render(request, 'portal/my_courses.html', context)


def my_courses(request):
    # After user login is implemented.
    # courses_registered = student_course.objects.filter(id=request.user.user_id)

    current_student = Students.objects.get(user= request.user.id)
    Branch_of_study = current_student.branch
    my_courses_list = [i.Course.course_title for i in current_student.student_course_set.all()]
    courses_registered = [Course.objects.get(course_title=i) for i in my_courses_list]

    context = {'courses_registered': courses_registered, 'branch': Branch_of_study}
    return render(request, 'portal/my_courses.html', context)

class forgotPassword(TemplateView):
    template_name = 'portal/forgot_password.html'

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,{})

    def post(self,request,*args,**kwargs):
        email = request.POST['email']
        try:
            valid_user = User.objects.get(username=email)
            temp_password = "sainath"
            valid_user.set_password(temp_password)
        except User.DoesNotExist:
            return render(request,self.template_name,{'error_message':"Invalid Email"})
        send_mail("Temporary password", "Your temporary password is " + temp_password , "sainath.b14@iiits.in",
                  ['sainath.b14@iiits.in'])
        return HttpResponseRedirect('/login')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer