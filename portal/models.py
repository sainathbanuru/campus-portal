from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.
from django.contrib.auth.models import User
from administration.models import *


class Notices(models.Model):
    notice_title = models.CharField(max_length=80)
    notice_description = models.TextField()

    def __str__(self):
        return self.notice_title


class Events(models.Model):
    event_title = models.CharField(max_length=80)
    event_date = models.DateField()
    event_duration = models.PositiveIntegerField()
    event_description = models.TextField()
    event_contact = models.CharField(max_length=50)
    event_user = models.CharField(max_length=50)

    def __str__(self):
        return self.event_title
    def event_month(self):
        month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                       'November', 'December']
        return month_names[self.event_date.month - 1]
    def get_absolute_url(self):
        return reverse('events',kwargs={'pk':self.pk})

class Forum(models.Model):
    thread_title = models.CharField(max_length=50)
    thread_description = models.TextField()
    thread_tag = models.CharField(max_length=15)
    thread_user = models.CharField(max_length=20)


    def __str__(self):
        return self.thread_title


class formRequest(models.Model):
    form_name = models.CharField(max_length=50)
    form_fathersName = models.CharField(max_length=50)
    form_required = models.CharField(max_length=50)
    form_reason = models.CharField(max_length=100)
    form_status = models.CharField(max_length=50,default='processing')

    def __str__(self):
        return self.form_name + "-" + self.form_required

class Credits(models.Model):
    flexi_core = models.IntegerField()
    bouquet_core = models.IntegerField()
    it_elective = models.IntegerField()
    maths_science = models.IntegerField()
    humanities = models.IntegerField()
    skills = models.IntegerField()
    btp = models.IntegerField()
    free_elective = models.IntegerField()

    def __str__(self):
        return "Credit details"

class Students(models.Model):
    user = models.OneToOneField(User)
    fathers_name = models.CharField(max_length=80)
    roll_no = models.CharField(max_length=10)
    email = models.EmailField()
    phone=models.CharField(max_length=10)
    branch = models.CharField(max_length=5)
    year = models.IntegerField()

    def __str__(self):
        return self.user.get_full_name()


class Student_Course(models.Model):

    Course = models.ForeignKey(Course, on_delete=models.CASCADE)
    Student = models.ForeignKey(Students, on_delete=models.CASCADE)

    def __str__(self):
        return self.Student.user.get_full_name() + " - " + self.Course.course_title
