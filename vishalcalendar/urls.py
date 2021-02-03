"""vishalcalendar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from scheduler.views import *
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', loginreg, name='home'),
    url(r'^inviteUser/', inviteUser, name='inviteUser'),
    url(r'^userhome', userhome, name='userhome'),
    url(r'^viewVal/', viewVal, name='viewVal'),
    url(r'^userschedules/', userschedules, name='userschedules'),
    url(r'^addInvite/', addInvite, name='addInvite'),
    url(r'^loginpage', loginpage, name='loginpage'),
    url(r'^asched', asched, name='asched'),
    url(r'^shedadd', shedadd, name='shedadd'),
    url(r'^changedates', changedates, name='changedates'),
    url(r'^login_check', login_check, name='login_check'),
    url(r'^register', register, name='register'),
]
