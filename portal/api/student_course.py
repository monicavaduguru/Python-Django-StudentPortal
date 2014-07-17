from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from tastypie.utils import trailing_slash
from django.conf.urls import url
import logging as log
from portal.models import Batch,Student,Course,Enroll
from course import CourseResource

class StudentResource(ModelResource):
    class Meta:
        resource_name = 'student'
        allowed_methods = ['get','post','put','delete']
        list_allowed_methods = ['post', 'get']
        serializer = Serializer(formats=['json'])
        authorization = Authorization()
        always_return_data = True

    def full_dehydrate(self, bundle, for_list=False):
        print 'in dehydrate'
        resp = []
        print bundle.obj
        resp = super(StudentResource,self).full_dehydrate(bundle)
        resp.data['course'] = bundle.obj.batch.courseId
        resp.data['coursename'] = bundle.obj.batch.courseId.coursename


        resp.data['prof']  = bundle.obj.batch.prof.first_name+bundle.obj.batch.prof.last_name
        resp.data['lechall']  = str(bundle.obj.batch.lectureHall.roomNumber)+' '+str(bundle.obj.batch.lectureHall.building)
        resp.data['quarter']  = bundle.obj.batch.quarter
        resp.data['year']  = bundle.obj.batch.year
        resp.data['grade']  = bundle.obj.grade
        resp.data['ta']  = bundle.obj.grade
        resp.data.pop('resource_uri')
        return resp

    def obj_get_list(self, bundle, request=None, **kwargs):
        try:
            e =  Enroll.objects.filter(studentId__user_id=kwargs['stdid'])
            return e
        except Exception as e:
            print e

    def obj_get(self, bundle, request=None, **kwargs):
        return Enroll.objects.filter(studentId=kwargs['stdid'])

    def obj_create(self, bundle, request=None,**kwargs):
        try:
            s = Student.objects.get(user_id=kwargs['stdid'])
            c = Course.objects.get(courseid=bundle.data.get('cid'))
            b = Batch.objects.get(quarter=bundle.data.get('quarter'),year=bundle.data.get('year'),
                                      courseId__courseid=bundle.data.get('cid'))
            if not b or not s or not c:
                return None

            en = Enroll.objects.filter(studentId=s,batch=b)
            if en :
                print 'already created'
                bundle.obj = en[0]
                return bundle

            fee = c.Credits * 200
            e = Enroll(studentId=s,batch=b,fee =fee)
            e.save()
            bundle.obj = e
            return bundle
        except Exception as e:
            print e

    def dispatch(self, request_type, request, **kwargs):
        if kwargs.get('pk'):
            kwargs['pk'] = kwargs.get('pk') if kwargs.get('pk')[-1] != '/' else kwargs.get('pk')[0:-1]
        return super(StudentResource, self).dispatch(request_type, request, **kwargs)

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<stdid>[\w-]*)/course%s$" %
                (self._meta.resource_name, trailing_slash())
                , self.wrap_view('handle_student_course_request')),
        ]

    def handle_student_course_request(self, request, **kwargs):
        log.debug('handle student course request')
        kwargs['resource_name'] = 'student'
        if kwargs.get('cid'):
            req_type = 'list'
        else:
            req_type = 'detail'
        return StudentResource().dispatch('list', request, **kwargs)


