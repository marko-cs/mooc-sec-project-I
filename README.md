# mood-sec-project-I

This project has been created for course [Cyber Security Base 2023 - Project I](https://cybersecuritybase.mooc.fi/module-3.1). 

# Project

Project repository is available in [Github](https://github.com/marko-cs/mood-sec-project-I). 

## Install and set-up

### Install

This project uses only standard Python packages and Django framework. Most connivent way to install needed is follow [course page instructions](https://cybersecuritybase.mooc.fi/installation-guide) if your staring from scratch. Follow those instructions for python and other library installations. 

If you have working python installation Django can be installed with pip.
```
pip install django
```

For application installation git clone should be sufficient.
```
git clone git@github.com:marko-cs/mooc-sec-project-I.git
```

If you don't have git installed all needed can be downloaded in one zip file. 

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

# Flaws
## A01:2021 – Broken Access Control

With broken access control user can view or manipulate data which is not owned or managed by particular user.

Login is required to view any data in application. That use Django build in login functionality. User can see only own data.
- [views.index_view](https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L16)

In this application user can delete only own records. Delete functionality checks that curren user is also owner of record to be deleted. If that is not the case deletion is not done and warning log entry is created. See details in 
- [views.delete_view](https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L37) 

## A03:2021 – Injection

Inputs from users can contain harmful content which reads, deletes or inserts data.  

All data manipulation done using Django objects to prevent SQL injection on statements. Raw or prepared SQL statements are not used at all. Data selections are based on server side information, not user inputs or parameters. 
- [views.index_view](https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/views.py#L16) 

## A07:2021 – Identification and Authentication Failures

Authentication and session management is critical for application security. General recommendation is use standard framework functionality for that. 

This application invalidates session if browser is closed to prevent session highjack in case of shared machine. Session lifetime is also made shorter comparing to standard. Both changes are visible in settings.
- [settings.py](https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/secprojectI/settings.py#L153)
- [settings.py] (https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/secprojectI/settings.py#L156)


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
- [login.html](https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/templates/flawsapp/login.html#L10)
- [index.html](https://github.com/marko-cs/mooc-sec-project-I/blob/main/secprojectI/flawsapp/templates/flawsapp/index.html#L34)   
