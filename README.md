# mood-sec-project-I

This project has been created for course https://cybersecuritybase.mooc.fi/module-3.1. 

# Project

Project repository is available at https://github.com/marko-cs/mood-sec-project-I. 

## Install and set-up

### Install

This project uses only standard Python packages and Django framework. If you are starting from scratch the most convenient way to install needed is follow course installation guide https://cybersecuritybase.mooc.fi/installation-guide. Follow those instructions for python and other library installations.
If you have a working python installation Django can be installed with pip.

```
pip install django
```

For application installation git clone should be sufficient.
```
git clone git@github.com:marko-cs/mooc-sec-project-I.git
```

If you don't have git installed all needed can be downloaded in one zip file Github web page. 

### Set-up

No specific set-up is needed, all needed configuration and data comes with git repository.
Additional users can be added with Django shell according example below

```
python3 manage.py shell
Python 3.10.6 (main, Aug 30 2022, 05:12:36) [Clang 13.1.6 (clang-1316.0.21.2.5)]
Type 'copyright', 'credits' or 'license' for more information
IPython 8.5.0 -- An enhanced Interactive Python. Type '?' for help.

from django.contrib.auth.models import User
user = User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")
user = User.objects.create_user("matt", "matt@black.com", "mattpassword")
:                                                                                                                           
Do you really want to exit ([y]/n)? y
```

Application can be started using Django manage.py and runserver command. 
```
python manage.py runserver
```
By default the application can be accessed using URL 127.0.0.1:8000/flawsapp/. There are two users created with credentials as in the above example.

# Flaws

Application is a simple web application storing URL and notes related to that. Each record is owned by users in the system. 

## A01:2021 – Broken Access Control

Link to source https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L64

With broken access control users can view or manipulate data which is not owned or managed by a particular user. By default Django applications don't require authentication and anyone knowing URL can use that functionality to delete any records. On secure applications there should be 
- Deny by default principle: Only authorized users can use such critical functionality such as delete and
- Enforce data ownership: Only the owner of data should be able to manipulate data, not any or all users.


**How to fix**
- With decorator it is easy to ensure that only authorized users can use functionality and that way enforce deny by default. We should add decorator @login_required(login_url='login/') to delete_view https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L67
- There should be check that authorized user can delete only own records https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L80 and to enforce ownership and not allowing users to delete any record.
- When user is removed also related records are deleted automatically https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/models.py#L9 to maintain data ownership. 

## A09:2021 – Security Logging and Monitoring Failures

Links to source 
- https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L74
- https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L99
- https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L115

Hostile parties can conduct forbidden activities within the application without getting noticed if logging is not planned and implemented well. Planned logging creates visibility on e.g. possible brute force attacks, data ownership breaches and critical application events. If application admins do not have that information available, it is not possible to monitor applications, react to events and do forensic analysis after security or other incidents.    

On secure application there should be: 
- Systematic logging convention for relevant content and format for log entries. Critical events such as data changes, logins, both successful and failed, should be logged in clear, structured format. 
- Generated log files should not be stored only locally.   

**How to fix**
- Default log configuration should be changed so that entries are created into log files. That should be changed in settings https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/secprojectI/settings.py#L127.
- Critical events such as creation https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L38 or  deletion https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L74 should be logged. And those created log entry should be in easily consumable format https://dev.splunk.com/enterprise/docs/developapps/addsupport/logging/loggingbestpractices/
- Logs should be collected from local storage to centralized location to prevent tampering or deletion. Also log file retention times should log enough to enable e.g. forensic analysis. And suspicious events should be detected. All that can be done with additional log monitoring tools such Splunk https://www.splunk.com/en_us/products/splunk-enterprise.html.   
- Log entries are created when user logs in https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L101 and out https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L117. 


## A03:2021 – Injection

Link to source https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L28

Inputs from users can contain harmful content which reads, deletes or inserts data. Typical injections are SQL injections where and attacker tries to manipulate data using SQL statements which are embedded into data provided by the end user. Objective is to execute those on the application server side. 

This application does not use Django framework features to prevent SQL injection. Instead we are using raw SQL and string operations to build those. 

**How to fix**

- By default Django provides Object Relational Mapping Tools. Those should be used for data and database record management instead of SQL statements. New record creation uses Django objects https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L44 only, not raw or prepared statements. 
- Data type for URL is Django URLField which comes with validation rules https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/models.py#L12 for correct format.


## A07:2021 – Identification and Authentication Failures

Links to source
- https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L88
- https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/secprojectI/settings.py#L155
- https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/secprojectI/settings.py#L160

Authentication and session management is critical for application security. General recommendation is to use standard framework functionality for that. Framework defaults for session management and login implementation are not following best practices.

Implemented login functionality checks only if user name and password is matching. That does not prevent brute force or dictionary attacks. 

The Django application framework does not by default invalidates the sessions if the browser is closed. That needs to be changed by a developer who is using a framework.  

**How to fix**

This application invalidates session if browser is closed https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/secprojectI/settings.py#L158. Default is not to do that. After this change sessions can not be retrieved that easily in the case of a shared machine. 

Session lifetime https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/secprojectI/settings.py#L162 has been set.

Install and configure django-axes module https://django-axes.readthedocs.io/en/latest/ to prevent brute force and dictionary attacks. That module can be used to set the number of failed login events and other restrictions to login events.   


## Cross-site Request Forgery

Links to source
- https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/templates/flawsapp/login.html#L10
- https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/templates/flawsapp/index.html#L34  

A CSRF attacker tries to trick innocent end users by sending a request that benefits the attacker. CSFR miss uses trust that the  receiving web application has towards the end user: the end user is login and authenticated and web the application assumes that the received request is valid and the end user has sent that intentionally. This can be done by providing a fake link to the end user during a valid session into a web application. 

**How to fix**

Django framework has build capability to prevent CSRF. All forms should contain crsf_toke which is a secret, unique and unpredictable value that is generated to protect form instances. With crsf_toke the application is sure that information from the form is related to something that the end user has requested during a valid session.

In this application build in functionality can take into use by un-commenting csrf_token tag in login.html https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/templates/flawsapp/login.html#L10 and index.html https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/templates/flawsapp/index.html#L34. 
