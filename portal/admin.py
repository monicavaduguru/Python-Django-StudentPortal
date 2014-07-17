from django.contrib import admin
from portal.models import Student,CommonUserData,Login,Major,Professor,PhoneNumber,Course,\
    Prereq,Admin,Timings,LectureHall,Batch,Enroll,Links,University

class LoginAdmin(admin.ModelAdmin):
    list_display = ('Username','Password')
admin.site.register(Login,LoginAdmin)

class CommonUserDataAdmin(admin.ModelAdmin):
    list_display = ('user_id','first_name','last_name')
admin.site.register(CommonUserData,CommonUserDataAdmin)

class MajorAdmin(admin.ModelAdmin):
    list_display = ('majorname','building')
admin.site.register(Major,MajorAdmin)

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('user_id','first_name','last_name','major')
admin.site.register(Professor,ProfessorAdmin)

admin.site.register(PhoneNumber)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('courseid','coursename','Credits','major')
admin.site.register(Course,CourseAdmin)

class PrereqAdmin(admin.ModelAdmin):
    list_display = ('course_id','prereq_id')
admin.site.register(Prereq,PrereqAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user_id','first_name','last_name','major')
admin.site.register(Student)

admin.site.register(Admin)

class HallAdmin(admin.ModelAdmin):
    list_display = ('roomNumber','building')
admin.site.register(LectureHall,HallAdmin)

class TimingsAdmin(admin.ModelAdmin):
    list_display = ('day','start_time','duration')
admin.site.register(Timings,TimingsAdmin)

class EnrollAdmin(admin.ModelAdmin):
    list_display = ('studentId','batch','grade')
admin.site.register(Enroll,EnrollAdmin)

class BatchAdmin(admin.ModelAdmin):
    list_display = ('courseId','quarter','year','prof','timings','lectureHall')
admin.site.register(Batch,BatchAdmin)

class LinksAdmin(admin.ModelAdmin):
    list_display = ('linkName','URL','program')
admin.site.register(Links,LinksAdmin)

class UniversityAdmin(admin.ModelAdmin):
    list_display = ('program','pricePerUnit')
admin.site.register(University,UniversityAdmin)





# Register your models here.
