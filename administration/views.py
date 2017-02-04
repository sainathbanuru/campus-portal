from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from administration.models import Course
from .forms import *
from portal.models import *
# Create your views here.

class admin_index(TemplateView):
    template_name = 'administration/admin_index.html'


class add_courses(FormView):
    template_name = 'administration/add-courses.html'
    form_class = courses

    def get(self, request, *args, **kwargs):
        form = self.form_class(None)
        courses_added = Course.objects.all()
        context = {
            'form' : form,
            'courses_added' : courses_added,
            'all_notices' : Notices.objects.all()
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = courses(request.POST)
        course_ug1,course_ug2,course_ug3,course_ug4 = False,False,False,False
        if "coursefor_ug1" in request.POST:
            course_ug1 = True
        if "coursefor_ug2" in request.POST:
            course_ug2 = True
        if "coursefor_ug3" in request.POST:
            course_ug3 = True
        if "coursefor_ug4" in request.POST:
            course_ug4 = True

        course_type = request.POST['course_type']
        if int(course_type) == 1:
            coursefor_cse = "flexi_core"
            coursefor_ece = "flexi_core"
        if int(course_type) == 2:
            coursefor_cse = "flexi_core"
            coursefor_ece = "it_elective"
        if int(course_type) == 3:
            coursefor_cse = "it_elective"
            coursefor_ece = "flexi_core"
        if int(course_type) == 4:
            coursefor_cse = "bc_cse"
            coursefor_ece = "it_elective"
        if int(course_type) == 5:
            coursefor_cse = "it_elective"
            coursefor_ece = "bc_ece"
        if int(course_type) == 6:
            coursefor_cse = "ms_elective"
            coursefor_ece = "ms_elective"
        if int(course_type) == 7:
            coursefor_cse = "humanities"
            coursefor_ece = "humanities"
        if int(course_type) == 8:
            coursefor_cse = "skills"
            coursefor_ece = "skills"
        if form.is_valid():
            course = Course(
                course_title=request.POST['course_title'],
                course_faculty=request.POST['course_faculty'],
                course_credits=request.POST['course_credits'],
                coursefor_ug1=course_ug1,
                coursefor_ug2=course_ug2,
                coursefor_ug3=course_ug3,
                coursefor_ug4=course_ug4,
                course_cse=coursefor_cse,
                course_ece=coursefor_ece,
                course_sem=request.POST['course_sem']
            )
            course.save()
        return HttpResponseRedirect('/administration/add-courses/')
'''
class add_notice(FormView):
    template_name = 'administration/add-notice.html'
    form_class = Notice
    def post(self, request, **kwargs):
        form = Notice(request.POST)
        if form.is_valid():
            notice = Notices(
                notice_title=request.POST['notice_title'],
                notice_description=request.POST['notice_description']
            )
            notice.save()
        return HttpResponseRedirect('administration/')


class add_notice(TemplateView):
    template_name = 'administration/add-notice.html'
    def post(self,request):
        notice = Notices(
            notice_title= request.POST['notice_title'],
            notice_description=request.POST['notice_description']
        )
        notice.save()
        return HttpResponseRedirect('administration/')
'''


def addNotice(request):
    if request.method =="GET":
        context = {
            'all_notices':Notices.objects.all()
        }
        return render(request, 'administration/add-notice.html', context)
    if request.method =="POST":
        notice = Notices(
            notice_title=request.POST['notice_title'],
            notice_description=request.POST['notice_description']
        )
        notice.save()
        return HttpResponseRedirect('/administration/')


def updateFormStatus(request):
    if request.method == 'GET':
        return render(request,'administration/form_status.html',{})
    if request.method =='POST':
        req_id = request.POST['search_id']
        return HttpResponseRedirect('/administration/update/' + req_id)


def FormStatus(request,search_id):
    if request.method == 'GET':
        try :
            requested_form = formRequest.objects.get(id=search_id)
            return render(request, 'administration/form_status.html',{'requested_form':requested_form})
        except formRequest.DoesNotExist:
            return render(request, 'administration/form_status.html',{'error_message':"Enter Valid ID"})
    if request.method == 'POST':
        status = request.POST['status']
        updated = formRequest.objects.get(id=search_id)
        updated.form_status = status
        updated.save()
        return HttpResponseRedirect('/')
