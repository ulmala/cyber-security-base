# Cyber Security Base 2022 Project 1

## Polls app

Link to the GitHub repository: https://github.com/ulmala/cyber-security-base

With this Polls app users can create their own custom polls and vote on polls created by other users. Only registered user should be able to create polls and vote. Users which are not registered can only view polls and their results, so they shouldn't be allowed to create polls or vote on existing ones.  

This app contains five flaws from [OWASP Top Ten list](https://owasp.org/www-project-top-ten/) 

## Installation

1. clone repository to your device
2. create virtual environment: `python -m venv .venv`
3. activate virtual environment: `source .venv/bin/activate`
4. install requirements: `pip install -r requirements.txt`
5. cd to "mysite" and run `python manage.py runserver`
6. go to http://127.0.0.1:8000/polls/ with your browser

## Flaws

### <ins>FLAW 1: [Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/) 

Flaw in source code [here](https://github.com/ulmala/cyber-security-base/blob/main/mysite/mysite/settings.py#L88).  

This application has authentication weakness. When creating a new user, either regular user or admin user, the application permits using weak passwords and well known passwords. Weak and well known passwords are easier to be guessed (e.g. brute force technics)

How to produce: For example it is possible to configure a superuser "admin" with password "admin", by running:
```code
    python manage.py createsuperuser
    >> Username (leave blank to use 'asd'): admin
    >> Email address:      
    >> Password: 
    >> Password (again): 
    >> Superuser created successfully.
```

Or one can create regular user by navigating to http://127.0.0.1:8000/polls/register and creating user with username "asd" and password "asd".  

How to fix:  
This flaw can be fixed by uncommenting lines 89-100 from [here](https://github.com/ulmala/cyber-security-base/blob/main/mysite/mysite/settings.py#L88). Then the app will then validate the passwords when creating user (e.g. validates that the password is not too common or the password does not contain any words from the given username).   

### <ins>FLAW 2: [Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/) 

Flaw in source code [here](https://github.com/ulmala/cyber-security-base/blob/main/mysite/polls/views.py#L75).  

This application has a flaw in access control which allows non registered users to create polls which should be only enabled for registered users (which is logged in).  

How to produce:  
The default way to create a poll should be by clicking the "Create" link on the navigation bar. The link is only visible for logged in users, that is checked in template `layout.html` in [this line](https://github.com/ulmala/cyber-security-base/blob/dff56297f04851ca16807f8b145f5d4b12baa239/mysite/polls/templates/polls/layout.html#L9).

But this is not enough, because it is not validated in the backend that the user is logged in. One can navigate to http://127.0.0.1:8000/polls/create (when not logged in) and the poll creation form is displayed and it can be filled and then submitted to the system.  

How to fix:  
To fix this flaw it needs to be validated also in the backend that the user is logged in. This can be done by uncommeting [this line](https://github.com/ulmala/cyber-security-base/blob/dff56297f04851ca16807f8b145f5d4b12baa239/mysite/polls/views.py#L75). 

### <ins>FLAW 3: [Security Logging and Monitoring Failures](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/)

Flaws in source code:
* [settings.py](https://github.com/ulmala/cyber-security-base/blob/c6d2d339d94c6e1f6d1cfc18e36d8f3a6a6447f0/mysite/mysite/settings.py#L123)
* polls/views.py lines: [13](https://github.com/ulmala/cyber-security-base/blob/c6d2d339d94c6e1f6d1cfc18e36d8f3a6a6447f0/mysite/polls/views.py#L13), [62](https://github.com/ulmala/cyber-security-base/blob/c6d2d339d94c6e1f6d1cfc18e36d8f3a6a6447f0/mysite/polls/views.py#L62) and [74](https://github.com/ulmala/cyber-security-base/blob/c6d2d339d94c6e1f6d1cfc18e36d8f3a6a6447f0/mysite/polls/views.py#L74)

This application has no logging features configured. It is important to log differenet types of events what happens in the application. This way it is easier to confirm possible breaches, analyse which caused the possible breach etc.  

 How to fix:  
 One needs to uncomment lines mentioned above. After this a logger is configured in `mysite/settings.py` file and it is used in `mysite/polls/views.py` to log every login and logout. Logs can be found from `mysite/logs/debug.log`. To only log logins and logouts is not enough so more logging should be added to the application as well.

### <ins>FLAW 4: [Security Misconfiguration](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)  
Flaw in source code [here](https://github.com/ulmala/cyber-security-base/blob/c6d2d339d94c6e1f6d1cfc18e36d8f3a6a6447f0/mysite/mysite/settings.py#L26)

This application has a security configuration error in the server settings. Variable DEBUG is set to True even though there is a mention that it should be set to False in production use. If there is some unhandled error in the source code, view with detailed error message is returned to the user if the error occures. This can give the attacker more information how to breach the application, e.g. information that outdated external package is used.  

How to produce this error: When not logged in navigate to http://127.0.0.1:8000/polls/logout in the browser. Since no user is not logged in and GET request is not handled in the function [logout_](https://github.com/ulmala/cyber-security-base/blob/c6d2d339d94c6e1f6d1cfc18e36d8f3a6a6447f0/mysite/polls/views.py#L71) and the DEBUG variable is set to True, the server will return a view which has detailed information about the application.  

How to fix: 
* Variable [DEBUG](https://github.com/ulmala/cyber-security-base/blob/c6d2d339d94c6e1f6d1cfc18e36d8f3a6a6447f0/mysite/mysite/settings.py#L26) needs to be set to True and "127.0.0.1" needs to be added to list [ALLOWED_HOSTS](https://github.com/ulmala/cyber-security-base/blob/c6d2d339d94c6e1f6d1cfc18e36d8f3a6a6447f0/mysite/mysite/settings.py#L28) (when running this application locally)
* Uncomment [this](https://github.com/ulmala/cyber-security-base/blob/0319faea6cf8a04ed0b780e82f30f16a695895c6/mysite/polls/views.py#L76) line so if other than POST request is done, application is redirected to index page.

### <ins> FLAW 5: [Vulnerable and Outdated Components](https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/)

Flaw in source code [here](https://github.com/ulmala/cyber-security-base/blob/703688bcb145511eddb6ece4c75cbdeb2c648e9f/requirements.txt#L1)

This application is using old version of Django, version 2.1 which was released in 2018. When checking the Django [documentation of the release](https://docs.djangoproject.com/en/2.1/) it says "This document is for an insecure version of Django that is no longer supported. Please upgrade to a newer release!".

How to fix:  
Upgrade Django to the latest version (4.1.4 at the moment when writing this) by running `pip install --upgrade django`.  

And finally update dependency file by runnning `pip freeze > requirements.txt`.