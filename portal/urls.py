from django.conf.urls import url,include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet.as_view())


urlpatterns = [
    url(r'^$',views.index.as_view(),name="index"),
    url(r'^events/$',views.events.as_view(),name='events'),
    url(r'^almanac/$',views.almanac,name='almanac'),
    url(r'^timetable/$',views.timetable,name='timetable'),
    url(r'^requestform/$',views.requestForm.as_view(),name='requestForm'),
    url(r'^forum/$',views.forum,name='forum'),
    url(r'^register/$',views.register.as_view(),name='register'),
    url(r'^contact/$',views.contact,name='contact'),
    url(r'^addEvent/',views.addEvent,name='addevent'),
    url(r'^login/',views.login_user,name='userLogin'),
    url(r'^signup/',views.Signup.as_view(),name='signup'),
    url(r'^credits/',views.credits.as_view(),name='credits'),
    url(r'^logout/',views.logout_user,name='userLogout'),
    url(r'^changepassword/',views.changepassword,name='changepassword'),
    url(r'^forgotPassword/',views.forgotPassword.as_view(),name='forgotPassword'),
    url(r'^administration/',include('administration.urls')),

    url(r'^register_course/',views.register_course,name='register_course'),
    url(r'^register/$', views.register.as_view(), name='register'),
    url(r'^unregister/$', views.unregister.as_view(), name='unregister'),
    url(r'^unregister2/$', views.unregister2, name='unregister2'),
    url(r'^my_courses/',views.my_courses,name="my_courses"),
    url(r'^attendance/$', views.AttendanceDisplay.as_view(), name='attendance'),
    url(r'^suggestions/$', views.suggestions.as_view(), name='suggestions'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'users/',views.UserViewSet,name='user')

]