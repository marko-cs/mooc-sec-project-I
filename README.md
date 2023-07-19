# mood-sec-project-I

This project has been created for course [Cyber Security Base 2023 - Project I](https://cybersecuritybase.mooc.fi/module-3.1). 

# Project

Project repository is availabele in [Github](https://github.com/marko-cs/mood-sec-project-I). 

# Flaws
## A01:2021 – Broken Access Control

- Failed logins logged and "too many failed logins"
- Session removeal after logout

## A03:2021 – Injection

Input validation and prepared statemens, no string catenation 

## A05:2021 – Security Misconfiguration

- Custom http error pages in use to prevent any additonal information to be leaked in case of error. 
- Directory lisings disabled

## A07:2021 – Identification and Authentication Failures

Session time out set short. That can be exted after success full action.

## A09:2021 – Security Logging and Monitoring Failures

Logins and other critical actions logged into log file. This solution assumes that for log files there is external solution to collect those into centralized location and prevent altering. 