from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.admin_index.as_view(),name="admin_index"),
    url(r'^add-courses/$',views.add_courses.as_view(),name="add-course"),
    url(r'^addNotice/$',views.addNotice,name="addNotice"),
]