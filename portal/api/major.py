from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from tastypie.utils import trailing_slash
from django.conf.urls import url
import logging as log
from portal.models import Major
from course import CourseResource

class MajorResource(ModelResource):
    class Meta:
        resource_name = 'major'
        allowed_methods = ['get','post','put','delete']
        list_allowed_methods = ['post', 'get']

        serializer = Serializer(formats=['json'])
        queryset = Major.objects.all()
        authorization = Authorization()
        always_return_data = True


    def obj_get_list(self, bundle, request=None, **kwargs):
        return Major.objects.all()

    def obj_get(self, bundle, request=None, **kwargs):
        try:
            return Major.objects.get(majorname=kwargs.get('pk'))
        except:
            raise ObjectDoesNotExist('No object found')

    def obj_create(self, bundle, request=None,**kwargs):
        print 'obj create'

    def dispatch(self, request_type, request, **kwargs):
        print kwargs
        if kwargs.get('pk'):
            kwargs['pk'] = kwargs.get('pk') if kwargs.get('pk')[-1] != '/' else kwargs.get('pk')[0:-1]
        return super(MajorResource, self).dispatch(request_type, request, **kwargs)

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<mjid>[\w/-]*)/course%s$" %
                (self._meta.resource_name, trailing_slash())
                , self.wrap_view('handle_major_course_request')),
            url(r"^(?P<resource_name>%s)/(?P<mjid>[\w-]*)/course/(?P<pk>[\w-]*)%s$" %
                (self._meta.resource_name, trailing_slash())
                , self.wrap_view('handle_major_course_request')),

            url(r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash())
                , self.wrap_view('handle_major_request')),
            url(r"^(?P<resource_name>%s)/(?P<pk>[\w/-]*)%s$" %
                (self._meta.resource_name, trailing_slash())
                , self.wrap_view('handle_major_request')),
        ]

    def handle_major_course_request(self, request, **kwargs):
        log.debug('handle major course request')
        kwargs['resource_name'] = 'course'
        if kwargs.get('pk'):
            req_type = 'detail'
        else:
            req_type = 'list'
        return CourseResource().dispatch(req_type, request, **kwargs)

    def handle_major_request(self, request, **kwargs):
        log.debug('handle major request')
        kwargs['resource_name'] = 'major'
        if kwargs.get('pk'):
            req_type = 'detail'
        else:
            req_type = 'list'
        return MajorResource().dispatch(req_type, request, **kwargs)
