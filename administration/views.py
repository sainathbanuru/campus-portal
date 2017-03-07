from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView,CreateView
from administration.models import Course
from .forms import *
from portal.models import *
from datetime import date
import xlrd
import time



def check_attendance(request):
    if request.user.groups.filter(name='admin').exists():

        template_name = 'administration/check_attendance.html'
        data = {}
        courses = Course.objects.all()

        for course in courses:

            # Find all students who opted the course....
            students_opted = [i.Student for i in course.student_course_set.all()]
            for student in students_opted:

                student_name = student.user.get_full_name()

                # Compute attendance....
                absent_on = list(set([i.date for i in Attendance.objects.filter(student_rollno=student.roll_no).filter(course_title=course.course_title).filter(status="A") ]))


                '''# Converting date to a dic as follows - { Month1: [day1, day2, .. ], ..... }
                month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                month_dic = {}


                for date in absent_on:

                    t_month = month_names[ date.month - 1]
                    if t_month not in month_dic:
                        month_dic[t_month] = [date]
                    else:
                        month_dic[t_month] += [date]'''



                if course in data:
                    data[course][student_name] = absent_on

                else:
                    data[course] = {student_name: absent_on}





        context = {
            'data' : data,
            'all_notices' : Notices.objects.all()
        }

        return render(request, template_name, context)
    else:
        return HttpResponse("<h1>You are not authorized to use this page</h1>")



class AttendancefilesCreate(CreateView):
    model = Attendancefiles
    fields = ['file']



def admin_attendance(request, pk):
    if request.user.groups.filter(name='admin').exists():
        File = Attendancefiles.objects.get(pk=pk)
        File.get_path()
        file_location = File.name
        workbook = xlrd.open_workbook(file_location)
        months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

        # Need optimisation ..
        for n in range(0, workbook.nsheets):


            sheet = workbook.sheet_by_index(n)
            course = sheet.cell_value(2, 0)  # Subject: Course Title
            course = course.split(":")[1][1:]
            month_year = sheet.cell_value(2, 4).split()


            for i in range(5, sheet.nrows):

                roll_no = sheet.cell_value(i, 1)
                roll_no = str(roll_no).split(".")[0]
                roll_no = ''.join( [ ch for ch in roll_no if ch in "0123456789" ] )

                for j in range(4, sheet.ncols):

                    status = str( sheet.cell_value(i, j) )

                    # Storing only for absent ..
                    if status.upper() == "A":


                        #print "\n\n\n\n\n\n\n", sheet.cell_value(4, j), type(sheet.cell_value(4, j)), "\n\n\n\n\n\n\n"
                        day = int(sheet.cell_value(4, j))
                        month = months.index( month_year[0].lower() ) + 1
                        year = int( month_year[1] )

                        d = date(day=day, year=year, month=month)

                        try:

                            obj = Attendance.objects.get(student_rollno=roll_no, course_title=course, date=d)
                            obj.status = status
                            obj.save()
                            #print "fuck"

                        except:

                            student_attendance = Attendance()
                            student_attendance.student_rollno = roll_no
                            student_attendance.course_title = course
                            student_attendance.date = d
                            student_attendance.status = status
                            student_attendance.save()


            #time.sleep(1)

        context = {
            'value': "Data is stored in Database"
        }
        return render(request, 'administration/attendance_admin.html', context)
    else:
        return HttpResponse("<h1>You are not authorized to use this page</h1>")



class CreditdetailsCreate(CreateView):
    model = Creditdetails
    fields = ['file']



def get_first_row(sheet):

    # S.No | IS... |  | CSE/ECE | .....
    for i in range(sheet.nrows):

        #print "\n\n\n\n\n\n"
        #print sheet.cell_value(i, 0)
        #print sheet.cell_value(i, 1)
        #print sheet.cell_value(i, 3)
        #print "\n\n\n\n\n\n"

        if str( sheet.cell_value(i, 0) ) == "1" or str( sheet.cell_value(i, 0) ) == "1.0":
            if "IS" in str( sheet.cell_value(i, 1) ) or len( str( sheet.cell_value(i, 1) ) ) == 9:
                if str( sheet.cell_value(i, 3) ).upper() == "CSE" or str( sheet.cell_value(i, 3) ).upper() == "ECE":

                    return i



# Upon succesful Credit details file submission..
def Upload_success(request, pk):
    
    File = Creditdetails.objects.get(pk=pk)
    File.get_path()
    file_location = File.name
    workbook = xlrd.open_workbook(file_location)


    for excel_sheet in range(0, workbook.nsheets):
    
        sheet = workbook.sheet_by_index(excel_sheet)
        first_row = get_first_row(sheet)
        
        for i in range(first_row, sheet.nrows):

            counter = 0

            roll_no = sheet.cell_value(i, 1)
            roll_no = str(roll_no).split(".")[0]
            roll_no = ''.join( [ ch for ch in roll_no if ch in "0123456789" ] )


            # Checking if a record exists for currrent roll number, if yes deleting it
            try:
                Credits.objects.get(student_roll_no=roll_no).delete()
            except:
                pass
                
            
            credit_object = Credits()
            credit_object.student_roll_no =  roll_no
            
            # Total number of credits done...
            total = 0

            for j in range(4, sheet.ncols):

                if sheet.cell_value( first_row-1, j ) == "Credits Total":

                    if counter == 0:
                        credit_object.core = int(sheet.cell_value(i, j))
                        total += int(sheet.cell_value(i, j))

                    if counter == 1:
                        credit_object.bouquet_core = int(sheet.cell_value(i, j))
                        total += int(sheet.cell_value(i, j))

                    if counter == 2:
                        credit_object.it_elective = int(sheet.cell_value(i, j))
                        total += int(sheet.cell_value(i, j))

                    if counter == 3:
                        credit_object.skills = int(sheet.cell_value(i, j))
                        total += int(sheet.cell_value(i, j))

                    if counter == 4:
                        credit_object.science = int(sheet.cell_value(i, j))
                        total += int(sheet.cell_value(i, j))

                    if counter == 5:
                        credit_object.humanities = int(sheet.cell_value(i, j))
                        total += int(sheet.cell_value(i, j))

                    if counter == 6:
                        credit_object.maths = int(sheet.cell_value(i, j))
                        total += int(sheet.cell_value(i, j))

                    if counter == 7:
                        credit_object.btp_honors = int(sheet.cell_value(i, j))
                        total += int(sheet.cell_value(i, j))

                    if counter == 8:
                        credit_object.additional_projects = int(sheet.cell_value(i, j))
                        total += int(sheet.cell_value(i, j))


                    counter += 1



            credit_object.total_credits = total
            credit_object.save()            

    context = {
        'value': "Data is stored in Database"
    }
    return render(request, 'administration/upload_success.html', context)



class admin_index(TemplateView):
    template_name = 'administration/admin_index.html'

    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(name='admin').exists():
            return render(request,self.template_name,{})
        else:
            return HttpResponse("You are not authorized to use this page")



class add_courses(FormView):
    template_name = 'administration/add-courses.html'
    form_class = courses

    def get(self, request, *args, **kwargs):
        form = self.form_class(None)
        courses_added = Course.objects.all()
        if request.user.groups.filter(name='admin').exists():
            context = {
                'form' : form,
                'courses_added' : courses_added,
                'all_notices' : Notices.objects.all()
            }
        else:
            return HttpResponse("You are not authorized to use this page")
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
        
        if int(course_type) == 4:
            coursefor_cse = "Boquet Core"
            coursefor_ece = "IT Elective"
        
        if int(course_type) == 3:
            coursefor_cse = "IT Elective"
            coursefor_ece = "Flexi Core"
        
        if int(course_type) == 5:
            coursefor_cse = "IT Elective"
            coursefor_ece = "Boquet Core"
        
        if int(course_type) == 6:
            coursefor_cse = "IT Elective"
            coursefor_ece = "IT Elective"
        
        if int(course_type) == 7:
            coursefor_cse = "Maths/Science Elective"
            coursefor_ece = "Maths/Science Elective"
        
        if int(course_type) == 8:
            coursefor_cse = "Humanities Elective"
            coursefor_ece = "Humanities Elective"
        
        if int(course_type) == 9:
            coursefor_cse = "Skills Elective"
            coursefor_ece = "Skills Elective"
        
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
                course_ece=coursefor_ece
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
        if request.user.groups.filter(name='admin').exists():
            context = {
                'all_notices':Notices.objects.all()
            }
        else:
            return HttpResponse("You are not authorized to use this page")
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
        if request.user.groups.filter(name='admin').exists():
            pass
        else:
            return HttpResponse("You are not authorized to use this page")
        return render(request,'administration/form_status.html',{})
    if request.method =='POST':
        req_id = request.POST['search_id']
        return HttpResponseRedirect('/administration/update/' + req_id)


def FormStatus(request,search_id):
    if request.method == 'GET':
        if request.user.groups.filter(name='admin').exists():
            try :
                requested_form = formRequest.objects.get(id=search_id)
                return render(request, 'administration/form_status.html',{'requested_form':requested_form})
            except formRequest.DoesNotExist:
                return render(request, 'administration/form_status.html',{'error_message':"Enter Valid ID"})
        else:
            return HttpResponse("You are not authorized to use this page")
    if request.method == 'POST':
        status = request.POST['status']
        updated = formRequest.objects.get(id=search_id)
        updated.form_status = status
        updated.save()
        return HttpResponseRedirect('/')


class Files(TemplateView):
    template_name = 'administration/files.html'

    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(name='admin').exists():
            context = {
                'files': [Attendancefiles.objects.all()]
            }
        else:
            return HttpResponse("<h1>You are not authorized to use this page</h1>")
        return render(request, self.template_name, context)


class credit_upload(TemplateView):
    template_name = 'administration/credits_upload.html'

    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(name='admin').exists():
            return render(request,self.template_name,{})
        else:
            return HttpResponse("<h1>You are not authorized to use this page</h1>")





class add_almanac(FormView):
    template_name = 'administration/add-almanac.html'
    form_class = add_almanac

    def get(self, request, *args, **kwargs):
       form = self.form_class(None)
       context = {
            'form':form
       }
       return render(request,self.template_name,context)

    def post(self, request, *args, **kwargs):
        return HttpResponse('correct')
