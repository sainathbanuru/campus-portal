from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.admin_index.as_view(),name="admin_index"),
    url(r'^add-courses/$',views.add_courses.as_view(),name="add-course"),
    url(r'^addNotice/$',views.addNotice,name="addNotice"),
    url(r'^update/(?P<search_id>[0-9]+)/$', views.FormStatus, name="formupdatestatus"),
    url(r'^formStatusUpdate/$',views.updateFormStatus,name="formupdate"),
    #url(r'^(?P<album_id>[0-9]+)/$', views.detail, name="detail"),
    url(r'^admin_attendance/(?P<pk>[0-9]+)/$', views.admin_attendance, name="admin_attendance"),
    url(r'^attendance_upload/$', views.AttendancefilesCreate.as_view(), name="attendance_upload"),
    #url(r'^attendance_success/$', views.Attendance_admin.as_view(), name="attendance_success"),
    url(r'^files/$', views.Files.as_view(), name="files"),
    url(r'^credit_upload/$', views.credit_upload.as_view(), name="credit_upload"),
url(r'^upload_success/$', views.Upload_success.as_view(), name="upload_success"),
]