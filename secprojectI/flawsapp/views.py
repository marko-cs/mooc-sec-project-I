""" View definitions for the app """
import logging
from uuid import uuid4

from django.shortcuts import render, redirect
#from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.db import connection



from . import forms
from . import models

logger = logging.getLogger("sessions")

# Create your views here.


@login_required(login_url="login/")
def index_view(request):
    """ Login user """
    user = request.user
    url_notes = models.URLNotes.objects.filter(user=user)
    form_add = forms.AddURL()
    return render(
        request, "flawsapp/index.html", {"form_add": form_add, "notes": url_notes}
    )


@login_required(login_url="login/")
def addnew_view(request):
    """ Add new intem into DB: flaw version """
    if request.method == "POST":
        # A03:2021 – Injection
        # Input from user should be checked and validated
        notes = request.POST.get("notes", "")
        url = request.POST.get("url", "")
        uuid = uuid4()
        user = request.user.id
        sql = (
        f"INSERT INTO flawsapp_urlnotes (notes, url, uuid, user_id) "
        f"VALUES ('{notes}', '{url}', '{uuid}', {user});"
        )

        #(
        #"INSERT INTO flawsapp_urlnotes (notes, url, uuid, user_id) VALUES ('%s', '%s', '%s', %s);"
        #% (notes, url, uuid, user)
        #)
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        # A09:2021 – Security Logging and Monitoring Failures
        # When new data record is created, it should be logged into log
        # log_msg = "event=record added,  user=%s, session_key=%s " %(user, session_key)
        # logger.info(log_msg)
    return redirect("index")


# A03:2021 – Injection
# Fixed version for adding entry
@login_required(login_url="login/")
def addnew_view_fixed(request):
    """ Add new item: fixed version """
    if request.method == "POST":
        form = forms.AddURL(request.POST)
        user = request.user
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.save()
            # When new data record is created, it should be logged into log
            # session_key = request.session.session_key
            # log_msg = "event=record added,  user=%s, session_key=%s " %(user, session_key)
            # logger.info(log_msg)
    return redirect("index")


#
# A01:2021 – Broken Access Control
# No authentication or any access control required for critical functionality
# No record ownership check before delete
def delete_view(request, item_id):
    """ Delete item, with flaw """
    item = models.URLNotes.objects.get(uuid=item_id)
    # A09:2021 – Security Logging and Monitoring Failures
    # Deletion of record should be logged
    # user = request.user
    # session_key = request.session.session_key
    # log_msg = "event=record deleted,  user=%s, session_key=%s " %(str(user), session_key)
    # logger.info(log_msg)
    #
    # A01:2021 – Broken Access Control
    # Fixed: add ownership check
    if item.user == request.user:
        item.delete()
    return redirect("index")


# A07:2021 – Identification and Authentication Failures
# No counter for failed logins attempts and there fore allowing brute force and dictionary attacks
def login_view(request):
    """ Login, feel free to try brute force """
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if not request.session.session_key:
                request.session.create()
            # A09:2021 – Security Logging and Monitoring Failures
            # No log entries created
            #session_key = request.session.session_key
            # log_msg = "event=login,  user=%s, session_key=%s " %(str(user), session_key)
            # logger.info(log_msg)
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            return redirect("index")
    else:
        form = AuthenticationForm()
    return render(request, "flawsapp/login.html", {"form": form})


def logout_view(request):
    """ Log out without logging """
    if request.method == "POST":

        # A09:2021 – Security Logging and Monitoring Failures
        # No log entries created
        # session_key = request.session.session_key
        # user = request.user
        # log_msg = "event=logout,  user=%s, session_key=%s " %(str(user), session_key)
        # logger.info(log_msg)
        logout(request)
    return redirect("index")
