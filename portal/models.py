from django.db import models

# Create your models here.


class Notices(models.Model):
    notice_title = models.CharField(max_length=80)
    notice_description = models.TextField()

    def __str__(self):
        return self.notice_title