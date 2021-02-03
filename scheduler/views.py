from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse
from .models import *
import calendar
from .utils import EventCalendar
import calendar
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
# Create your views here.
notes, usr = "", ""
a=0

def loginreg(request):
    return render(request,'loginregister.html',{})

def loginpage(request):
    return render(request,'loginregister.html',{})

def register(request):
    fname= request.POST.get("fname")
    lname= request.POST.get("lname")
    email= request.POST.get("email")
    utype= request.POST.get("utype")
    username= request.POST.get("username")
    password= request.POST.get("password")
    print ("name,email,uname,paswd",fname,lname,utype,email,username,password)
    if utype=="Admin":
        obj=User(
            first_name=fname.upper(),last_name=lname,email=email,username=username,password=password,is_staff=True,is_superuser=True
            )
        obj.save()
        return HttpResponse("<script>alert('Registration Successful for Admin');window.location.href=/loginpage/;</script>")
    elif utype=="Staff":
        obj=User(
            first_name=fname.upper(),last_name=lname,email=email,username=username,password=password,is_staff=True
            )
        obj.save()
        return HttpResponse("<script>alert('Registration Successful for Staff');window.location.href=/loginpage/;</script>")
    else:
        obj=User(
            first_name=fname.upper(),last_name=lname,email=email,username=username,password=password
            )
        obj.save()
        
    print("registerd")
    return HttpResponse("<script>alert('Registration Successful');window.location.href=/loginpage/;</script>")

def login_check(request):
    print ("login_check(request):")
    if request.method=="POST":
        u=request.POST.get("username")
        p=request.POST.get("password")
        print ("in login page:",u,"::::",p)

        try:
            user_data=User.objects.get(username=u)
            request.session["user"] = u
            print(user_data.check_password(p))
            if user_data.is_superuser and user_data.check_password(p):
                return HttpResponse("<script>alert('Welcome Admin');window.location.href=/admin/;</script>")
            elif user_data.check_password(p) or str(p)==user_data.password:
                return HttpResponse("<script>alert('Welcome "+user_data.first_name+"');window.location.href=/userhome/;</script>")
            else:
                return HttpResponse("<script>alert('Please register');window.location.href=/loginpage/;</script>")
        except Exception as ex:
            print("Exception: ",ex)
            return HttpResponse("<script>alert('Please register first');window.location.href=/loginpage/;</script>")
    else:
        return HttpResponse("<script>alert('Some issues');window.location.href=/loginpage/;</script>")

def viewVal(request):
    global notes, usr, a
    users = User.objects.all()
    notes = request.GET.get("notes")
    usr = request.GET.get("user")
    print(a," --> ",notes, usr)
    a+=1
    eventsObj = Event.objects.get(notes=notes, username=usr)
    import datetime
    extra_context=None
    after_day= request.GET.get('day__gte', None)
    extra_context = extra_context or {}

    if not after_day:
        d = datetime.date.today()
    else:
        try:
            split_after_day = after_day.split('-')
            d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
        except:
            d = datetime.date.today()

    previous_month = datetime.date(year=d.year, month=d.month, day=1)  # find first day of current month
    previous_month = previous_month - datetime.timedelta(days=1)  # backs up a single day
    previous_month = datetime.date(year=previous_month.year, month=previous_month.month,
                                   day=1)  # find first day of previous month

    last_day = calendar.monthrange(d.year, d.month)
    next_month = datetime.date(year=d.year, month=d.month, day=last_day[1])  # find last day of current month
    next_month = next_month + datetime.timedelta(days=1)  # forward a single day
    next_month = datetime.date(year=next_month.year, month=next_month.month,
                               day=1)  # find first day of next month

    cal = EventCalendar(request.session['user'])
    html_calendar = cal.formatmonth(d.year, d.month, withyear=True)
    html_calendar = html_calendar.replace('<td ', '<td  width="150" height="150"')
    extra_context['calendar'] = mark_safe(html_calendar)
    return render(request, 'user_schedules.html', {"cont":str(extra_context['calendar']),"day":eventsObj.day, "endt": eventsObj.end_time, "startt": eventsObj.start_time, "notes":eventsObj.notes, "user":eventsObj.username, "invites":eventsObj.invites})
        

def inviteUser(request):
    global notes, usr, a
    users = User.objects.all()
    if a==0:
        notes = request.POST.get("notes")
        usr = request.POST.get("user")
        print(a," --> ",notes, usr)
        a+=1
        request.session["notes"] = notes
        request.session["usr"] = usr
    
    return render(request, 'invitation.html', {"data":users})

def userhome(request):
    print("User Home")
    return render(request,"user_home.html",{})

def changedates(request):
    import datetime
    extra_context=None
    after_day= request.GET.get('day__gte', None)
    extra_context = extra_context or {}

    if not after_day:
        d = datetime.date.today()
    else:
        try:
            split_after_day = after_day.split('-')
            d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
        except:
            d = datetime.date.today()

    previous_month = datetime.date(year=d.year, month=d.month, day=1)  # find first day of current month
    previous_month = previous_month - datetime.timedelta(days=1)  # backs up a single day
    previous_month = datetime.date(year=previous_month.year, month=previous_month.month,
                                   day=1)  # find first day of previous month

    last_day = calendar.monthrange(d.year, d.month)
    next_month = datetime.date(year=d.year, month=d.month, day=last_day[1])  # find last day of current month
    next_month = next_month + datetime.timedelta(days=1)  # forward a single day
    next_month = datetime.date(year=next_month.year, month=next_month.month,
                               day=1)  # find first day of next month

    cal = EventCalendar(request.session['user'])
    html_calendar = cal.formatmonth(d.year, d.month, withyear=True)
    html_calendar = html_calendar.replace('<td ', '<td  width="150" height="150"')
    extra_context['calendar'] = mark_safe(html_calendar)
    return HttpResponse(extra_context['calendar'])

def userschedules(request):
    import datetime
    extra_context=None
    after_day= None
    extra_context = extra_context or {}

    if not after_day:
        d = datetime.date.today()
    else:
        try:
            split_after_day = after_day.split('-')
            d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
        except:
            d = datetime.date.today()

    previous_month = datetime.date(year=d.year, month=d.month, day=1)  # find first day of current month
    previous_month = previous_month - datetime.timedelta(days=1)  # backs up a single day
    previous_month = datetime.date(year=previous_month.year, month=previous_month.month,
                                   day=1)  # find first day of previous month

    last_day = calendar.monthrange(d.year, d.month)
    next_month = datetime.date(year=d.year, month=d.month, day=last_day[1])  # find last day of current month
    next_month = next_month + datetime.timedelta(days=1)  # forward a single day
    next_month = datetime.date(year=next_month.year, month=next_month.month,
                               day=1)  # find first day of next month

    cal = EventCalendar(request.session['user'])
    html_calendar = cal.formatmonth(d.year, d.month, withyear=True)
    html_calendar = html_calendar.replace('<td ', '<td  width="150" height="150"')
    extra_context['calendar'] = mark_safe(html_calendar)
    return render(request,"htmlcalendar.html",{"cont":str(extra_context['calendar'])})

def asched(request):
    return render(request, 'add_user_sched.html', {})

def shedadd(request):
    days = request.POST.getlist('day')
    startt = request.POST.getlist('startt')
    endt = request.POST.getlist('endt')
    notes = request.POST.getlist('notes')
    print("--> ",days, startt, endt, notes, request.user, request.session['user'])
    eventsObj = Event(day=days[0], start_time=startt[0], end_time=endt[0], notes=notes[0], username=request.session['user'], invites= request.session['user']).save()
    return HttpResponse("<script>alert('Successfully Scheduled');window.location.href=/asched/;</script>")

def addInvite(request):
    global notes, usr
    tasks = request.GET.getlist('tasks[]')
    print("----****===",notes)
    print("----****===",usr)
    print(tasks,len(tasks))
    if len(tasks)>10:
        return HttpResponse('Cannot add invite more than 10 Users')
    try:
        eventsObj = Event.objects.get(notes=notes)
        a = str(eventsObj.invites)+","+",".join(tasks)
        l = a.split(",")
        if len(l)>10:
            return HttpResponse('Cannot add invite more than 10 Users')
        eventsObj.invites = a
        eventsObj.save()
    except Exception as ex:
        print("Ex: ",ex)
        return HttpResponse('Some Error Occured')
    return HttpResponse('Success')
