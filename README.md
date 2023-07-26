# mood-sec-project-I

This project has been created for course [Cyber Security Base 2023 - Project I](https://cybersecuritybase.mooc.fi/module-3.1). 

# Project

Project repository is available in [Github](https://github.com/marko-cs/mood-sec-project-I). 

## Install and set-up

### Install

- django
- django extensions

### Set-up
``````
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
``````
# Flaws
## A01:2021 – Broken Access Control

With broken access control user can view or manipulate data which is not owned or managed by particular user.

In this application user can delete only own records. Delete functionality checks that curren user is also owner of record to be deleted. If that is not the case deletion is not done and warning log entry is created. See details in 
- [views.delete_view](https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L37) 

## A03:2021 – Injection

Inputs from users can contain harmful content which reads, deletes or inserts data.  

All data manipulation done using Django objects to prevent SQL injection on statements. Raw or prepared SQL statements are not used at all. Data selections are based on server side information, not user inputs or parameters. 
- [views.index_view](https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L16) 


## A05:2021 – Security Misconfiguration

- Custom http error pages in use to prevent any additional information to be leaked in case of error. 
- Directory listings disabled

## A07:2021 – Identification and Authentication Failures

Session time out set short. That can be extended after success full action.

## A09:2021 – Security Logging and Monitoring Failures

Critical events such as logins, both success full and failed as well high value data changes should be logged. 

This solution assumes that for log files there is external solution to collect those into centralized location and prevent altering. Created logs contains related session id information so that those can easily correlated in particular session.  

Added log configuration is not production ready entries are created into console. That can be easily changed without any code changes. 
- [settings.LOGGING](https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/secprojectI/settings.py#L127)

Log entries are created when user logs in and out. 
- [views.login_view](https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L49)
- [views.logout_view](https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L68)

## Cross-site Request Forgery

CSRF attacker tries to trick innocent end user send request that benefits attacker. CSFR miss uses trust that receiving web application has towards end user: end user is login and authenticated and web application assumes that received request is valid and end user has send that intentionally. 

Django framework has build capability to prevent CSRF. All forms should contain `crsf_toke` which is secret, unique and unpredictable value that is generated to protect form instance. 
- [login.html](https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/templates/flawsapp/login.html)
- [index.html] (https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/templates/flawsapp/index.html)   