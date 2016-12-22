from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index,name="index"),
    url(r'^events/$',views.events,name='events'),
    url(r'^almanac/$',views.almanac,name='almanac'),
    url(r'^timetable/$',views.timetable,name='timetable'),
    url(r'^requestform/$',views.requestForm,name='requestForm'),
    url(r'^contact/$',views.contact,name='contact'),
    url(r'^addEvent/',views.addEvent,name='addevent'),
    url(r'^login/',views.login_user,name='userLogin'),
    url(r'^logout/',views.logout_user,name='userLogout'),
    url(r'^changepassword/',views.changepassword,name='changepassword'),
]