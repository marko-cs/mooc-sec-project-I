from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.db import connection
import logging
from uuid import uuid4


from . import forms
from . import models  

logger = logging.getLogger("sessions")

# Create your views here.

@login_required(login_url='login/')
def index_view(request):
    user = request.user 
    URLNotes = models.URLNotes.objects.filter(user=user)
    form_add = forms.AddURL()
    return render(request, 'flawsapp/index.html', {'form_add': form_add, 'notes': URLNotes})

@login_required(login_url='login/')
def addnew_view(request):
    if request.method == 'POST':
        # A03:2021 – Injection
        # Input from user should be checked and validated
        notes = request.POST.get('notes', '')
        url = request.POST.get('url', '')
        uuid = uuid4()
        user = request.user.id
        sql = "INSERT INTO flawsapp_urlnotes (notes, url, uuid, user_id) VALUES ('%s', '%s', '%s', %s);" %(notes, url, uuid, user)
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        # A09:2021 – Security Logging and Monitoring Failures
        # When new data record is created, it should be logged into log
        #log_msg = "event=record added,  user=%s, session_key=%s " %(user, session_key)
        #logger.info(log_msg) 
    return redirect('index')  

# A03:2021 – Injection
# Fixed version for adding entry 
@login_required(login_url='login/')
def addnew_view_fixed(request):     
    if request.method == 'POST':
        form = forms.AddURL(request.POST)
        user = request.user
        session_key = request.session.session_key   
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.save()
            # When new data record is created, it should be logged into log
            #log_msg = "event=record added,  user=%s, session_key=%s " %(user, session_key)
            #logger.info(log_msg)
        return redirect('index')        
    else:
        return redirect('index')

#
# A01:2021 – Broken Access Control 
# No authentication or any access control required for critical functionality 
# No record ownership check before delete 
def delete_view(request, id):
    user = request.user
    session_key = request.session.session_key
    #
    # 
    # 
    item = models.URLNotes.objects.get(uuid=id)
    # A09:2021 – Security Logging and Monitoring Failures
    # Deletion of record should be logged 
    # log_msg = "event=record deleted,  user=%s, session_key=%s " %(str(user), session_key)
    # logger.info(log_msg)
    item.delete()
    #
    # A01:2021 – Broken Access Control
    # How to fix: add ownership check 
    #if item.user == user:   
    #    item.delete()
    return redirect('index')



# A07:2021 – Identification and Authentication Failures
# No counter for failed logins attempts and there fore allowing brute force and dictionary attacks 
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            # A09:2021 – Security Logging and Monitoring Failures
            # No log entries created 
            #log_msg = "event=login,  user=%s, session_key=%s " %(str(user), session_key)
            #logger.info(log_msg)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'flawsapp/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        session_key = request.session.session_key
        user = request.user
        # A09:2021 – Security Logging and Monitoring Failures
        # No log entries created 
        #log_msg = "event=logout,  user=%s, session_key=%s " %(str(user), session_key)
        #logger.info(log_msg)
        logout(request)
        return redirect('index')
