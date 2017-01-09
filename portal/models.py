from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.


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
