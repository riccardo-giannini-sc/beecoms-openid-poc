from django.views.generic import View
from django.http import HttpResponse

from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout

from django.conf import settings
from django.core.exceptions import PermissionDenied

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
        with open(os.path.join(settings.BASE_DIR, 'POC/secrets.json')) as client_info:
            data = json.loads(client_info.read())
            client_id = data["client_id"]
        return HttpResponse(client_id)


'''
curl -X POST -H "Cache-Control: no-cache" -H "Content-Type: application/x-www-form-urlencoded" "http://127.0.0.1:8002/o/token/"
-d "client_id=3acdP8a40lynGYntwY6JwG5a1VF3ZgofPtuC7aNy"
-d "client_secret=NDBUxvjMPffa1bZlGmF9vlGN9XxMOf74xb5WAQin2qr5Cxo8KuroncjvMyCgBZplYsIecbs8SMuExkdWiQgfRhxwwXdjpvKbmJzEIt8vQSxt1vicFGGDZX6n6F0BXVlP"
-d "code=Lpq9a8H8rCx9qDqFaG8a9pntpUN26c"
-d "redirect_uri=http://127.0.0.1:8000/authcode"
-d "grant_type=authorization_code"
'''
class auth_code(View):
    def dispatch(self, *args, **kwargs):
        return super(auth_code, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):

        code = request.POST.get( "code" )
        redirect_uri = request.POST.get( "redirect_uri" )

        with open(os.path.join(settings.BASE_DIR, 'POC/secrets.json')) as client_info:
            data = json.loads(client_info.read())
            client_id = data["client_id"]
            client_secret = data["client_secret"]

        post_data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }
        post_headers = {
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        #response = requests.post('http://layer:8001/token/', data = post_data, headers = post_headers)
        response = requests.post('http://prm:8000/o/token/', data = post_data, headers = post_headers)

        return HttpResponse(response.content)

class prm_resource(View):
    def dispatch(self, *args, **kwargs):
        return super(prm_resource, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        #response = requests.get('http://layer:8001/resource/')
        response = requests.get('http://prm:8000/resource/')
        if response.status_code == 403:
            raise PermissionDenied()
        return HttpResponse(response.content, status = response.status_code)
