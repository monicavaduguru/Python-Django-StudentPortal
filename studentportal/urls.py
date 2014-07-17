from django.conf.urls import patterns, include, url

from django.contrib import admin
from tastypie.api import Api
from portal.api.major import MajorResource
from portal.api.course import CourseResource
from portal.api.student_course import StudentResource
from portal.api.student import StudentMainResource

from portal.views import *

from django.conf import settings
from django.conf.urls import patterns, url

admin.autodiscover()
v1_api = Api(api_name='v1')
v1_api.register(MajorResource())
v1_api.register(CourseResource())
v1_api.register(StudentResource())
v1_api.register(StudentMainResource())



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'studentportal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^api/',include(v1_api.urls)),
    url(r'^login/?',handle_login),
    url(r'^logout/?',handle_logout),
    url(r'^admin/?', include(admin.site.urls)),
    url(r'^Course_History/',handle_course_history),
    url(r'^Personal_Information/',handle_personal_information),
    url(r'^Add_Courses/',handle_course_add),
    url(r'^Drop_Courses/',handle_course_delete),
    url(r'^Fee/',handle_fee),
    url(r'^Grades/',handle_grades),
    url(r'^Important_Links/',handle_links),
    url(r'^/?',handle_main),
    #url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
    #(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),

)
