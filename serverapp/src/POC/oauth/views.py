from django.views.generic import View
from django.views.generic.base import TemplateView
from django.http import HttpResponse

from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout

from django.conf import settings
from django.core.exceptions import PermissionDenied

from .models import AccessToken, RefreshToken, AppUser

import json
import requests
import os
import datetime
import secrets
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

from base64 import b64encode, b64decode



class homepage(TemplateView):
    template_name = 'login.html'


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
            app_user_obj = AppUser.objects.get(username = username)
            if app_user_obj.salt == None:
                salt = secrets.token_bytes(32)
                app_user_obj.salt = salt
                app_user_obj.save()

            privkey = PBKDF2HMAC(
                algorithm = hashes.SHA256,
                length = 32,
                salt = app_user_obj.salt,
                iterations = 32000
            ).derive(password.encode())

            request.session['privkey'] = b64encode(privkey).decode('utf-8')

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
        print(request.user)
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

        body = json.loads( request.body )
        code = body.get( "code" )
        redirect_uri = body.get( "redirect_uri" )

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
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        response = requests.post('http://layer:8001/auth_code/', data = post_data, headers = post_headers)
        return HttpResponse(response.content, status = response.status_code)
        # response = requests.post('http://prm:8000/o/token/', data = post_data, headers = post_headers)

        json_response = json.loads( response.content )

        if response.status_code == 200:
            access_token = json_response['access_token']
            refresh_token = json_response['refresh_token']


            # ENCRYPTING TOKENS

            app_user_obj = AppUser.objects.get(username = request.user.username )
            if 'privkey' in request.session:
                current_privkey = request.session['privkey'].encode()
                f = Fernet(current_privkey)
                protected_access_token = f.encrypt(access_token.encode())
                protected_refresh_token = f.encrypt(refresh_token.encode())
                access_token_obj = AccessToken.objects.create(
                     user = app_user_obj,
                     token = protected_access_token,
                     expires = datetime.datetime.now() + datetime.timedelta(0, json_response['expires_in']),
                     scope = json_response['scope']
                )
                refresh_token_obj = RefreshToken.objects.create(
                     user = app_user_obj,
                     token = protected_refresh_token,
                     access_token = access_token_obj,
                )
            else:
                return HttpResponse("[ERROR] - No private key")


        return HttpResponse(str(json_response), status = response.status_code)

class prm_resource(View):
    def dispatch(self, *args, **kwargs):
        return super(prm_resource, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):


        # DECRYPTING TOKENS
        current_privkey = None
        if 'privkey' in request.session:

            app_user_obj = AppUser.objects.get(username = request.user.username )
            current_privkey = request.session['privkey'].encode()
            f = Fernet(current_privkey)
            access_token_obj = AccessToken.objects.filter(user = app_user_obj).last()
            access_token = f.decrypt(access_token_obj.token).decode('utf-8')

            headers = { 'Authorization': 'Bearer ' + access_token }

            response = requests.get('http://layer:8001/resource/', headers = headers)

            if response.status_code == 403:
                raise PermissionDenied()
        else:
            return HttpResponse("[ERROR] - No private key")
        return HttpResponse(response.content, status = response.status_code)
