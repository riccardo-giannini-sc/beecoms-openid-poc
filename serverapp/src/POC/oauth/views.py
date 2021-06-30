from django.views.generic import View
from django.http import HttpResponse

from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout

from django.conf import settings

import json
import requests
import os


class login(View):
    def dispatch(self, *args, **kwargs):
        return super(login, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        body = json.loads( request.body )
        username = body.get( "username" )
        password = body.get( "password" )
        user_obj = authenticate( request, username = username, password = password)
        if user_obj != None and user_obj.is_authenticated:
            auth_login(request, user_obj)
            return HttpResponse("[SUCCESS] - Logged in")
        return HttpResponse("[ERROR] - Credentials", status = 401)

class logout(View):
    def dispatch(self, *args, **kwargs):
        return super(logout, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        auth_logout(request)
        return HttpResponse("[SUCCESS] - Logged out")

class client_id(View):
    def dispatch(self, *args, **kwargs):
        return super(client_id, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponse("Simple HTTP response\n")

class auth_code(View):
    def dispatch(self, *args, **kwargs):
        return super(auth_code, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = requests.post('http://layer:8001/token/')
        return HttpResponse(response.content)

class prm_resource(View):
    def dispatch(self, *args, **kwargs):
        return super(prm_resource, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        response = requests.get('http://layer:8001/resource/')
        return HttpResponse(response.content)
