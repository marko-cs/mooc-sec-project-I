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

- Failed logins logged and "too many failed logins"
- Session removal after logout

## A03:2021 – Injection

Input validation and prepared statements, no string catenation 

## A05:2021 – Security Misconfiguration

- Custom http error pages in use to prevent any additional information to be leaked in case of error. 
- Directory listings disabled

## A07:2021 – Identification and Authentication Failures

Session time out set short. That can be exted after success full action.

## A09:2021 – Security Logging and Monitoring Failures

Logins and other critical actions logged into log file. This solution assumes that for log files there is external solution to collect those into centralized location and prevent altering. 

- Log configuration
- Logged events
    - User login and logout
    - Data entry created or deleted 