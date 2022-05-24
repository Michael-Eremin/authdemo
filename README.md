# AUTHDEMO

##Description

The service demonstrates signed user name and password verification. The information is transmitted to the server via Coockie or Form.

##Project composition

#####Functionality:

* Getting a validation request to the server through the main '/' page using Coockie
* Getting a validation request to the server through the 'login/' page using Form
* Creating a digital signature
* Getting username from a signed string
* Password verification


##Development Requirements

####Python 3.10.0

* fastapi
* base64
* hmac
* hashlib
* typing
* json

####Packages(pip_requirements.txt):

* anyio==3.5.0
* asgiref==3.5.0
* click==8.0.3
* fastapi==0.73.0
* h11==0.13.0
* idna==3.3
* pydantic==1.9.0
* python-multipart==0.0.5
* six==1.16.0
* sniffio==1.2.0
* starlette==0.17.1
* typing-extensions==4.0.1
* uvicorn==0.17.4*


##Code start

Terminal - command: **uvicorn server:app --reload**.