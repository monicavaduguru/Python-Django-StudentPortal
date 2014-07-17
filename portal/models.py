from django.db import models
#from composite_field import CompositeField
from django.contrib.auth.models import User

class Login(models.Model):
    Username=models.CharField(max_length=30,primary_key=True)
    Password=models.CharField(max_length=30)
    def __unicode__(self):
         return self.Username


class CommonUserData(models.Model):
    user_id=models.CharField(max_length=6,primary_key=True)
    first_name=models.CharField(max_length=30,null=True,blank=True)
    last_name=models.CharField(max_length=30,null=True,blank=True)
    dob=models.DateField(null=True,blank=True)
    address_housenum=models.CharField(max_length=10,null=True,blank=True)
    address_street=models.CharField(max_length=30,null=True,blank=True)
    address_city=models.CharField(max_length=20,null=True,blank=True)
    address_pin=models.CharField(max_length=10,null=True,blank=True)
    username=models.OneToOneField(Login,null=True,blank=True)
    def __unicode__(self):
        return (self.user_id)



class Admin(CommonUserData):
    #SalaryId=models.CharField(max_length=6)
    Salary=models.DecimalField(max_digits=10,decimal_places=2)
    def __unicode__(self):
        return self.first_name+self.last_name

class PhoneNumber(models.Model):
    user_id=models.ForeignKey(CommonUserData)
    phoneNumber=models.CharField(max_length=10,primary_key=True)
    def __unicode__(self):
        return self.phoneNumber

class Major(models.Model):
    majorname=models.CharField(max_length=30,primary_key=True)
    building=models.CharField(max_length=30)
    def __unicode__(self):
         return self.majorname

class Professor(CommonUserData):
    salary=models.DecimalField(max_digits=10,decimal_places=2)
    major=models.ForeignKey(Major)
    def __unicode__(self):
         return self.first_name+" "+self.last_name


class Course(models.Model):
    courseid=models.CharField(max_length=10,primary_key=True)
    coursename=models.CharField(max_length=30)
    Credits=models.IntegerField(max_length=1)
    major=models.ForeignKey(Major)
    prereqid=models.ManyToManyField('self',symmetrical=False,through='Prereq',related_name='course_prereq')
    def __unicode__(self):
         return self.coursename+'_'+self.major.majorname

class Prereq(models.Model):
    course_id=models.ForeignKey(Course,related_name='course_id')
    prereq_id=models.ForeignKey(Course,related_name='prereq_id')
    def __unicode__(self):
        return self.course_id+self.prereq_id

    class Meta:
        unique_together=("course_id","prereq_id")

class University(models.Model):
    program=models.CharField(max_length=30,primary_key=True)
    pricePerUnit=models.DecimalField(max_digits=6,decimal_places=2)
    major=models.ManyToManyField(Major)
    def __unicode__(self):
        return self.program

class Links(models.Model):
    linkName=models.CharField(max_length=30,primary_key=True)
    URL=models.CharField(max_length=100)
    program=models.ForeignKey(University)

class Timings(models.Model):
    id=models.CharField(max_length=5,primary_key=True)
    day=models.CharField(max_length=10)
    start_time=models.CharField(max_length=10)
    duration=models.CharField(max_length=10)
    def __unicode__(self):
        return self.day+self.duration+self.start_time

    class Meta:
        unique_together=("day","start_time","duration")

class LectureHall(models.Model):
    roomNumber=models.IntegerField(max_length=4)
    building=models.CharField(max_length=30)
    capacity=models.IntegerField(max_length=4)
    def __unicode__(self):
        return str(self.roomNumber)+self.building

    class Meta:
        unique_together=("roomNumber","building")


class Batch(models.Model):
    quarter =models.CharField(max_length=10)
    year    =models.CharField(max_length=10)
    strength=models.IntegerField(max_length=3,blank=True,null=True)
    courseId=models.ForeignKey(Course)
    timings=models.ForeignKey(Timings)
    lectureHall=models.ForeignKey(LectureHall)
    prof =models.ForeignKey(Professor)

    def __unicode__(self):
         return self.quarter+'_' + self.year+'_'+self.courseId.coursename

    class Meta:
        unique_together=("courseId","quarter","year")

class Student(CommonUserData):
    #GPA=models.DecimalField(max_digits=2,decimal_places=1,blank=True,null=True)
    #Credits=models.IntegerField(max_length=2,null=True,blank=True)
    DateJoined=models.DateField(null=True,blank=True)
    major=models.ForeignKey(Major)
    program=models.ForeignKey(University)
    advisor=models.ForeignKey(Professor)
    batch=models.ManyToManyField(Batch,through='Enroll',null=True,blank=True)



class Enroll(models.Model):
    #fee=models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)
    grade=models.CharField(max_length=2,null=True,blank=True)
    studentId=models.ForeignKey(Student)
    batch=models.ForeignKey(Batch)
    def __unicode__(self):
         return self.studentId.user_id + self.batch.quarter+self.batch.year+ self.batch.courseId.coursename
    class Meta:
        unique_together=("studentId","batch")





