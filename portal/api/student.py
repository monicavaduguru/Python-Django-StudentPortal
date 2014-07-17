from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from tastypie.utils import trailing_slash
from django.conf.urls import url
import logging as log
from portal.models import Student
from course import CourseResource

class StudentMainResource(ModelResource):
    class Meta:
        resource_name = 'studentmain'
        allowed_methods = ['get']
        #list_allowed_methods = ['post', 'get']

        serializer = Serializer(formats=['json'])
        queryset = Student.objects.all()
        authorization = Authorization()
        always_return_data = True



    def obj_get(self, bundle, request=None, **kwargs):
        try:
            return Student.objects.get(user_id=kwargs.get('pk'))
        except:
            raise ObjectDoesNotExist('No object found')

    def dispatch(self, request_type, request, **kwargs):
        print kwargs
        if kwargs.get('pk'):
            kwargs['pk'] = kwargs.get('pk') if kwargs.get('pk')[-1] != '/' else kwargs.get('pk')[0:-1]
        return super(StudentMainResource, self).dispatch(request_type, request, **kwargs)

    def prepend_urls(self):
        return [

            url(r"^(?P<resource_name>%s)/(?P<pk>[\w/-]*)%s$" %
                (self._meta.resource_name, trailing_slash())
                , self.wrap_view('handle_studentMain_request')),
        ]



    def handle_studentMain_request(self, request, **kwargs):
        log.debug('handle student request')
        kwargs['resource_name'] = 'StudentMain'
        if kwargs.get('pk'):
            req_type = 'detail'

        return StudentMainResource().dispatch(req_type, request, **kwargs)
