from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView,CreateView
from administration.models import Course
from .forms import *
from portal.models import *
# Create your views here.
import xlrd
import time

class CreditdetailsCreate(CreateView):
    model = Creditdetails
    fields = ['file']

class Upload_success(TemplateView):
    template_name = 'administration/upload_success.html'

class admin_index(TemplateView):
    template_name = 'administration/admin_index.html'

class AttendancefilesCreate(CreateView):
    model = Attendancefiles
    fields = ['file']



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
            coursefor_cse = "Flexi Core"
            coursefor_ece = "Flexi Core"
        if int(course_type) == 2:
            coursefor_cse = "Flexi Core"
            coursefor_ece = "IT Elective"
        if int(course_type) == 3:
            coursefor_cse = "IT Elective"
            coursefor_ece = "Flexi Core"
        if int(course_type) == 4:
            coursefor_cse = "BC CSE"
            coursefor_ece = "IT Elective"
        if int(course_type) == 5:
            coursefor_cse = "IT Elective"
            coursefor_ece = "BC ECE"
        if int(course_type) == 6:
            coursefor_cse = "M/S Elective"
            coursefor_ece = "M/S Elective"
        if int(course_type) == 7:
            coursefor_cse = "Humanities"
            coursefor_ece = "Humanities"
        if int(course_type) == 8:
            coursefor_cse = "Skills"
            coursefor_ece = "Skills"
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


class Files(TemplateView):
    template_name = 'administration/files.html'

    def get(self, request, *args, **kwargs):
        context = {
            'files': [Attendancefiles.objects.all()]
        }
        return render(request, self.template_name, context)


class credit_upload(TemplateView):
    template_name = 'administration/credits_upload.html'

def admin_attendance(request, pk):
    file = Attendancefiles.objects.get(pk=pk)
    file.get_path()
    file_location = file.name
    workbook = xlrd.open_workbook(file_location)

    for n in range(0, workbook.nsheets - 1):

        sheet = workbook.sheet_by_index(n)
        course = sheet.cell_value(2,
                                  0)  # cell value with A3
        for i in range(5, sheet.nrows):

            rollno = str(sheet.cell_value(i, 1))

            students = Attendance.objects.filter(student_rollno=rollno, course_title=course)

            str_present = ""
            str_absent = ""
            for j in range(4, sheet.ncols):

                if sheet.cell_value(i, j) == "P":
                    str_present = str_present + str(sheet.cell_value(4, j)) + " " + sheet.cell_value(2, 4) + ","
                elif sheet.cell_value(i, j) == "A":
                    str_absent = str_absent + str(sheet.cell_value(4, j)) + " " + sheet.cell_value(2, 4) + ","

            if len(students) == 0 and rollno != '':

                b = Attendance()
                b.student_rollno = rollno
                b.course_title = course
                b.present = str_present
                b.absent = str_absent
                b.save()

            else:
                for student in students:
                    student.present = student.present + str_present
                    student.absent = student.absent + str_absent
                    student.save()
        time.sleep(1)

    context = {
        'value': "Data is stored in Database"
    }
    return render(request, 'administration/attendance_admin.html', context)


'''     for j in range(4, sheet.ncols):

            #print(sheet.cell_value(i, j))

            if len(students) == 0:
                #print("yes")
                b = Attendance()
                b.student_rollno = rollno
                b.course_title = course
                if sheet.cell_value(i, j) == "P":
                    b.present = str(sheet.cell_value(4, j)) + " " + sheet.cell_value(2, 4)
                elif sheet.cell_value(i, j) == "A":
                    b.abdent = str(sheet.cell_value(4, j)) + " " + sheet.cell_value(2, 4)
                b.save()
            else:
                #print("no")
                for student in students:
                    if student.course_title == course:
                        if sheet.cell_value(i, j) == "P":
                            #print(type(student.present))
                            student.present = student.present + "," + str(sheet.cell_value(4, j))+" "+sheet.cell_value(2, 4)

                        elif sheet.cell_value(i, j) == "A":
                            student.absent = student.absent + "," + str(sheet.cell_value(4, j))+" "+sheet.cell_value(2, 4)
                        student.save()'''
