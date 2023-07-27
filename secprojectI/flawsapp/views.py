from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
import logging

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
        form = forms.AddURL(request.POST)
        user = request.user
        session_key = request.session.session_key
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.save()
            log_msg = "event=record added,  user=%s, session_key=%s " %(user, session_key)
            logger.info(log_msg)
        return redirect('index')        
    else:
        return redirect('index')

@login_required(login_url='login/')
def delete_view(request, id):
    user = request.user
    session_key = request.session.session_key
    item = models.URLNotes.objects.get(uuid=id)
    if item.user == user:   
        item.delete()
        log_msg = "event=record deleted,  user=%s, session_key=%s " %(str(user), session_key)
        logger.info(log_msg)
    else:
        log_msg = "event=security event,  user=%s, session_key=%s, info=User %s trying to delete record owned by %s " %(str(user), session_key, user, item.user)
        logger.warning(log_msg)       
    return redirect('index')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            log_msg = "event=login,  user=%s, session_key=%s " %(str(user), session_key)
            logger.info(log_msg)
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
        log_msg = "event=logout,  user=%s, session_key=%s " %(str(user), session_key)
        logger.info(log_msg)
        logout(request)
        return redirect('index')
