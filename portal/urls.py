from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index.as_view(),name="index"),
    url(r'^events/$',views.events.as_view(),name='events'),
    url(r'^almanac/$',views.almanac,name='almanac'),
    url(r'^timetable/$',views.timetable,name='timetable'),
    url(r'^requestform/$',views.requestForm.as_view(),name='requestForm'),
    url(r'^forum/$',views.forum,name='forum'),
    url(r'^contact/$',views.contact,name='contact'),
    url(r'^addEvent/',views.addEvent,name='addevent'),
    url(r'^login/',views.login_user,name='userLogin'),
    url(r'^logout/',views.logout_user,name='userLogout'),
    url(r'^changepassword/',views.changepassword,name='changepassword'),
]