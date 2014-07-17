from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from tastypie.utils import trailing_slash
from django.conf.urls import url
import logging as log
from portal.models import Course

class CourseResource(ModelResource):
    class Meta:
        resource_name = 'course'
        allowed_methods = ['get', 'post', 'put', 'delete']
        serializer = Serializer(formats=['json'])
        queryset = Course.objects.all()
        authorization = Authorization()
        always_return_data = True

    def obj_get_list(self, bundle, request=None, **kwargs):
        return Course.objects.filter(**kwargs)

    def obj_get(self, bundle, request=None, **kwargs):
        try:
            return Course.objects.filter(**kwargs)
        except:
            raise ObjectDoesNotExist('No object found')

    def dispatch(self, request_type, request, **kwargs):
        if kwargs.get('pk'):
            kwargs['pk'] = kwargs.get('pk') if kwargs.get('pk')[-1] != '/' else kwargs.get('pk')[0:-1]
        if kwargs.get('pk'):
            kwargs['courseid'] = kwargs.get('pk')
        if kwargs.get('mjid'):
            kwargs['major__majorname'] = kwargs.get('mjid')
            del kwargs['mjid']
        print kwargs
        return super(CourseResource, self).dispatch(request_type, request, **kwargs)

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash())
                , self.wrap_view('handle_course_request')),
            url(r"^(?P<resource_name>%s)/(?P<pk>[\w/-]*)%s$" %
                (self._meta.resource_name, trailing_slash())
                , self.wrap_view('handle_course_request')),
        ]

    def handle_course_request(self, request, **kwargs):
        log.debug('handle major request')
        kwargs['resource_name'] = 'course'
        print 'in course'
        if kwargs.get('pk'):
            req_type = 'detail'
        else:
            req_type = 'list'
        return CourseResource().dispatch(req_type, request, **kwargs)