# mood-sec-project-I

This project has been created for course https://cybersecuritybase.mooc.fi/module-3.1. 

# Project

Project repository is available in https://github.com/marko-cs/mood-sec-project-I. 

## Install and set-up

### Install

This project uses only standard Python packages and Django framework. If your are staring from scratch most connivent way to install needed is follow course installation guide https://cybersecuritybase.mooc.fi/installation-guide. Follow those instructions for python and other library installations. 

If you have working python installation Django can be installed with pip.
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
Markos-MacBook-Air:secprojectI marko$ python3 manage.py shell
Python 3.10.6 (main, Aug 30 2022, 05:12:36) [Clang 13.1.6 (clang-1316.0.21.2.5)]
Type 'copyright', 'credits' or 'license' for more information
IPython 8.5.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from django.contrib.auth.models import User
   ...: 
In [2]: user = User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")

In [3]: user = User.objects.create_user("matt", "matt@black.com", "mattpassword")

In [4]:                                                                                                                            
Do you really want to exit ([y]/n)? y
```

Application can be started using Django manage.py and runserver command. 
```
python manage.py runserver
```
By default application can be accessed using URL http://127.0.0.1:8000/ 

# Flaws
## A01:2021 – Broken Access Control

With broken access control user can view or manipulate data which is not owned or managed by particular user.

to prevent this happen login is required to view or update any data in application. That use Django build in decorator and form handling functionality. 
- https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L15

After valid login user can see only own data.
- https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L18

In this application user can delete only own records. Delete functionality checks that curren user is also owner of record to be deleted. If that is not the case deletion is not done and warning log entry is created. 
- https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L38 

When user is removed also related records are deleted automatically to maintain data ownership.
- https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/models.py#L9

## A03:2021 – Injection

Inputs from users can contain harmful content which reads, deletes or inserts data. Typical injections are SQL injections where attacker tries to manipulate data using SQL statements which are embedded into data provided by end user. Objective is execute those on application server side. Another typical injection type is cross site scripting where attacker tries to inject code to be executed in client side.      

All data manipulation done using Django objects to prevent SQL injection on statements. Raw or prepared SQL statements are not used at all. 

New record creation uses Django objects only, not raw or prepared statements
- https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L24 

Same thing could be done with prepared SQL statements.
```python
cursor = conn.cursor()
sql = """INSERT INTO URLNotes (notes, url, user, uuid) VALUES (?, ?, ?, ?);"""
params_tuple=(notes, url, user, uuid)
cursor.execute(sql, parmas_tuple)
conn.commit()
```

Data type for URL is Django URLField which comes with validation rules for correct format.
- https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/models.py#L12

Data selections are based on server side information, not direct user inputs.
- https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L18 

## A07:2021 – Identification and Authentication Failures

Authentication and session management is critical for application security. General recommendation is use standard framework functionality for that. Framework defaults values in general and in this case session management particular should be reviewed and adjust according the needs.    

This application invalidates session if browser is closed. Default is not not do that. After this change sessions can not retrieved that easily in case of shared machine. 
- https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/secprojectI/settings.py#L153

Session lifetime is also made shorter comparing to standard setting.
- https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/secprojectI/settings.py#L156


## A09:2021 – Security Logging and Monitoring Failures

Critical events such as logins, both successful and failed, as well high value data changes should be logged. 

Application creates several log entries. All created logs contains related session id information so that those can easily correlated in particular session.  

Added log configuration is not production ready since log entries are created into console. That can be easily changed without any code changes. 
- https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/secprojectI/settings.py#L127

Log entries are created when user logs in and out. 
- https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L49
- https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L68

When user deletes own record or creates new one log entries is created for both. If user tries remove record without ownership warning log entry is created. 
- https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L39
- https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L23

This solution assumes that for log files there is external solution to collect those into centralized location and prevent altering.

## Cross-site Request Forgery

CSRF attacker tries to trick innocent end user send request that benefits attacker. CSFR miss uses trust that receiving web application has towards end user: end user is login and authenticated and web application assumes that received request is valid and end user has send that intentionally. This can be done by providing fake link to end user during valid session into web application. 

Django framework has build capability to prevent CSRF. All forms should contain crsf_toke which is secret, unique and unpredictable value that is generated to protect form instance. With crsf_toke application is sure that information from form is related to something that end user has requested during valid session.  
- https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/templates/flawsapp/login.html#L10
- https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/templates/flawsapp/index.html#L34  
