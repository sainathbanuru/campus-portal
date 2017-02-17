from django.db import models

# Create your models here.

class Course(models.Model):
    course_title = models.CharField(max_length=50)
    course_faculty = models.CharField(max_length=50)
    course_credits = models.IntegerField()
    coursefor_ug1 = models.BooleanField(default=False)
    coursefor_ug2 = models.BooleanField(default=False)
    coursefor_ug3 = models.BooleanField(default=False)
    coursefor_ug4 = models.BooleanField(default=False)
    course_cse = models.CharField(max_length=50)
    course_ece = models.CharField(max_length=50)
    course_sem = models.CharField(max_length=7)



    def __str__(self):
        return self.course_title + " - " + self.course_faculty

    class Attendance(models.Model):
        student_rollno = models.CharField(max_length=11)
        course_title = models.CharField(max_length=50)
        present = models.TextField(default="0-0-0000")
        absent = models.TextField(default="0-0-0000")

        def __str__(self):
            return self.student_rollno + " - " + self.course_title
