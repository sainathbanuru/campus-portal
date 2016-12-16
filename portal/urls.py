from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index,name="index"),
    url(r'^events/$',views.events,name='events'),
    url(r'^almanac/$',views.almanac,name='almanac'),
    url(r'^timetable/$',views.timetable,name='timetable'),
]