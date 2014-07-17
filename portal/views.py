from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext



from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django import forms
from models import *


@csrf_exempt
def handle_login(request):
    if request.META['REQUEST_METHOD'] == 'GET':
        print 'got into get of login'
        return render(request,'login.html')
    elif request.META['REQUEST_METHOD'] == 'POST':

        print request.POST.get('username')
        print request.POST.get('password')

        try:
            #l=Login.objects.filter(Username=request.POST.get('username'))
            #print "login matched"
            student=Student.objects.get(username__Username=request.POST.get('username'))
            response = HttpResponse('hello user ' + student.user_id)
            #print student.user_id
            response.set_cookie( 'userid', student.user_id)
            print response
            return response
        except Exception as e:
            print e


        # search for login user and mathc the password
        # if matched then load the common user
        # get the student object
        # set the cookie with studen id
        # reaturn studnet name in html object

        #else
        #show the login page again

def handle_main(request):
    try:
        #check if the cookie is right
        #send hello user
        #if no cookie render login
        userid =  request.COOKIES['userid']

        resp = HttpResponse('hello user '+ userid)
        print resp
        #return resp
        return render(request,'main.html')
    except Exception as e:
        print e
        return render(request,'login.html')
# Create your views here.

def handle_personal_information(request):
    try:
        userid =  request.COOKIES['userid']
        print userid
        s=Student.objects.get(user_id=userid)

        d={}
        d['id']=s.user_id
        d['firstname']=s.first_name
        d['lastname']=s.last_name
        d['dob']=s.dob
        d['hno']=s.address_housenum
        d['street']=s.address_street
        d['city']=s.address_city
        d['zip']=s.address_pin
        d['major']=s.major.majorname
        d['program']=s.program.program
        d['advisor']=s.advisor.first_name+ " "+s.advisor.last_name

        #context={dict:d}
        print d
        return render_to_response('personal_info.html',d,context_instance=RequestContext(request))
    except Exception as e:
        print e
        return render(request,'login.html')

def handle_course_history(request):
    try:
        userid =  request.COOKIES['userid']
        print userid
        s=Student.objects.get(user_id=userid)
        e=Enroll.objects.filter(studentId=s)
        prev_obj = []
        cur_obj = []

        for i in e:
            if i.grade != '' and i.grade != None:
                prev_obj.append(i)
            else:
                cur_obj.append(i)

        context={'e':prev_obj,'cur':cur_obj}
        print cur_obj
        #print e
        #print prev_obj

        return render(request, 'course_history.html', context)
        #for enrollobj in e:
         #   if (enrollobj.grade):
    except Exception as e:
        print e
        return render(request,'login.html')



MY_CHOICES = (
    ('1', 'Option 1'),
    ('2', 'Option 2'),
    ('3', 'Option 3'),
)


@csrf_exempt
def handle_course_add(request):
    try:
        userid =  request.COOKIES['userid']
        print userid
        s=Student.objects.get(user_id=userid)

        if request.META['REQUEST_METHOD'] == 'GET':
            batches=Batch.objects.filter(quarter='Q3',year='2014',courseId__major=s.major)
            choice=[]
            count=1
            for batchobj in batches:
                choice.append((batchobj.courseId.courseid,batchobj.courseId.coursename))
                count=count+1
                print choice


            @csrf_exempt
            class MyForm(forms.Form):
                my_choice_field = forms.ChoiceField(choices=choice)

            form = MyForm()
            return render_to_response('add_course.html',{'form': form,'batches':batches})
        else:
            try:
                cid=request.POST.get('my_choice_field')
                getbatch=Batch.objects.get(courseId__courseid=cid,quarter='Q3',year='2014')
            except Exception as e:
                print e
                return render(request,'nochoice.html')
            print cid
            print getbatch
            enrollList=Enroll.objects.filter(studentId=s)
            print enrollList
            for enrollobj in enrollList:
                if (enrollobj.batch.courseId.courseid==cid):
                    return render(request,'course_already_taken.html')
            e=Enroll(studentId=s,batch=getbatch)
            e.save()
            print e
            return render(request,'course_added.html')

    except Exception as e:
        print e
        return render(request,'login.html')


def handle_fee(request):

    try:
        userid =  request.COOKIES['userid']
        print userid
        s=Student.objects.get(user_id=userid)
        e=Enroll.objects.filter(studentId=s)
        cur_obj=[]
        prev_obj=[]
        for i in e:
            if i.grade != '' and i.grade != None:
                prev_obj.append(i)
            else:
                cur_obj.append(i)
        fee={}
        totalfee=0
        for obj in cur_obj:
            fee[obj.batch.courseId]=obj.batch.courseId.Credits*s.program.pricePerUnit
            totalfee=totalfee+obj.batch.courseId.Credits*s.program.pricePerUnit
        tosend={}
        if (totalfee!=0):
            tosend["totalfee"]=totalfee
        tosend["fee"]=fee
        return render_to_response('fee.html',tosend,context_instance=RequestContext(request))


    except Exception as e:
        print e
        return render(request,'login.html')


@csrf_exempt
def handle_course_delete(request):

    try:
        userid =  request.COOKIES['userid']
        print userid
        s=Student.objects.get(user_id=userid)
        cur_obj=[]
        prev_obj=[]
        e=Enroll.objects.filter(studentId=s)
        for i in e:
            if i.grade != '' and i.grade != None:
                prev_obj.append(i)
            else:
                cur_obj.append(i)

        if request.META['REQUEST_METHOD'] == 'GET':
            batches=Batch.objects.filter(quarter='Q3',year='2014')

            choice=[]
            count=0
            for cur in cur_obj:
                choice.append((cur.batch.courseId.courseid,cur.batch.courseId.coursename))
                count=count+1

            #for enrollobj in e:
             #   if enrollobj.grade=='' or enrollobj.grade==None:
              #      choice.append(enrollobj.batch.courseId.coursename)
               #     count=count+1

            @csrf_exempt
            class MyForm(forms.Form):
                my_choice_field = forms.ChoiceField(choices=choice)
            form = MyForm()
            return render_to_response('delete_course.html',{'form': form,'cur_obj':cur_obj,'count':count})
        else:
            try:
                cid=request.POST.get('my_choice_field')
                print cid
                enobj=Enroll.objects.get(studentId=s,batch__courseId__courseid=cid)

                #getbatch=Batch.objects.get(courseId__courseid=cid,quarter='q4',year='2014')
            except Exception as e:
                print e
                return render(request,'nochoice.html')
            print cid
            #print getbatch
            #enrollList=Enroll.objects.filter(studentId=s)
            #print enrollList
            #for enrollobj in enrollList:
            #    if (enrollobj.batch.courseId.courseid==cid):
             #       return render(request,'course_already_taken.html')
            #e=Enroll(studentId=s,batch=getbatch)
            #e.save()
            #print e
            print enobj
            enobj.delete()
            return render(request,'course_deleted.html')

    except Exception as e:
        print e
        return render(request,'login.html')


def handle_grades(request):
    try:
        userid =  request.COOKIES['userid']
        print userid
        s=Student.objects.get(user_id=userid)
        e=Enroll.objects.filter(studentId=s)
        gradedict={}
        quarterdict={}
        yeardict={}
        count=0
        totalpoints=0
        totalcredits=0

        for enrollobj in e:
            if enrollobj.grade != '' and enrollobj.grade != None:
                count+=1
                if (enrollobj.grade=='A'):
                    gradepoints=enrollobj.batch.courseId.Credits*4.0
                if (enrollobj.grade=='A-'):
                    gradepoints= enrollobj.batch.courseId.Credits*3.7
                if (enrollobj.grade=='B'):
                    gradepoints=enrollobj.batch.courseId.Credits*3.4
                if (enrollobj.grade=='B-'):
                    gradepoints=enrollobj.batch.courseId.Credits*3.1
                if (enrollobj.grade=='C'):
                    gradepoints=enrollobj.batch.courseId.Credits*2.8
                if (enrollobj.grade=='C-'):
                    gradepoints=enrollobj.batch.courseId.Credits*2.5
                if (enrollobj.grade=='D'):
                    gradepoints=enrollobj.batch.courseId.Credits*2.2
                if(enrollobj.grade=='F'):
                    gradepoints=enrollobj.batch.courseId.Credits*1.9
                totalpoints+=gradepoints
                yeardict[enrollobj]=enrollobj.batch.year
                quarterdict[enrollobj]=enrollobj.batch.quarter
                gradedict[enrollobj]=gradepoints
                totalcredits+=enrollobj.batch.courseId.Credits

        print totalcredits
        try:
            GPA=round(totalpoints/totalcredits,2)
        except Exception as e:
            print e
            GPA=0
        tosend={'gradedict':gradedict,'totalpoints':totalpoints,'GPA':GPA,'totalcredits':totalcredits,'yeardict':yeardict,'quarterdict':quarterdict}
        if (count!=0):
            tosend['count']=count
        return render_to_response('grades.html',tosend,context_instance=RequestContext(request))

    except Exception as e:
        print e
        return render(request,'login.html')

def handle_links(request):
    try:
        userid =  request.COOKIES['userid']
        s=Student.objects.get(user_id=userid)
        linkobj=Links.objects.filter(program=s.program)
        tosend={}
        tosend["linkobj"]=linkobj
        return render_to_response('links.html',tosend,context_instance=RequestContext(request))
    except Exception as e:
        print e
        return render(request,'login.html')
@csrf_exempt
def handle_logout(request):
    try:
        resp =  render(request,'login.html')
        resp.delete_cookie('userid')
        return resp
    except Exception as e:
        print e
        return render(request,'login.html')
