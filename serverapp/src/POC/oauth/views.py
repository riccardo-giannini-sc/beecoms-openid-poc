from django.views.generic import View
from django.views.generic.base import TemplateView
from django.http import HttpResponse

from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout

from django.conf import settings
from django.core.exceptions import PermissionDenied

from .models import AccessToken, RefreshToken, AppUser
from .utils import *

import json
import requests
import os
import datetime
import secrets
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

from base64 import b64encode, b64decode

class session(View):
    def dispatch(self, *args, **kwargs):
        return super(session, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse("User is logged in", status = 200)
        else:
            return HttpResponse("User not logged in", status = 401)

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

        json_response = json.loads( response.content )

        if response.status_code == 200:
            access_token = json_response['access_token']
            refresh_token = json_response['refresh_token']


            # ENCRYPTING TOKENS

            app_user_obj = AppUser.objects.get(username = request.user.username )
            if 'privkey' in request.session:
                current_privkey = request.session['privkey'].encode()
                access_token_obj = store_access_token(access_token, app_user_obj, json_response['expires_in'], json_response['scope'], current_privkey)
                refresh_token_obj = store_refresh_token(refresh_token, app_user_obj, access_token_obj, current_privkey)
            else:
                return HttpResponse("[ERROR] - No private key", status = 401)


        return HttpResponse(str(json_response), status = response.status_code)

class prm_resource(View):
    def dispatch(self, *args, **kwargs):
        return super(prm_resource, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        # DECRYPTING TOKEN
        current_privkey = None
        if 'privkey' in request.session:
            app_user_obj = AppUser.objects.get(username = request.user.username )
            current_privkey = request.session['privkey'].encode()
            f = Fernet(current_privkey)
            access_token_obj = AccessToken.objects.filter(user = app_user_obj).last()

            if access_token_obj != None:
                access_token = f.decrypt(access_token_obj.token).decode('utf-8')

                headers = { 'Authorization': 'Bearer ' + access_token }

                first_response = requests.get('http://layer:8001/resource/', headers = headers)

                # TOKEN EXPIRED
                if first_response.status_code == 401 and json.loads(first_response.content).get('error', '') == 'The access token has expired.':
                    # REFRESHING TOKEN
                    print(first_response.content)
                    post_data, post_headers = build_refresh_token_request(app_user_obj, f)
                    second_response = requests.post('http://layer:8001/auth_code/', data = post_data, headers = post_headers)

                    if second_response.status_code == 200:
                        json_response = json.loads( second_response.content )
                        access_token = json_response['access_token']
                        refresh_token = json_response['refresh_token']
                        access_token_obj = store_access_token(access_token, app_user_obj, json_response['expires_in'], json_response['scope'], current_privkey)
                        refresh_token_obj = store_refresh_token(refresh_token, app_user_obj, access_token_obj, current_privkey)
                        headers = { 'Authorization': 'Bearer ' + access_token }

                        third_response = requests.get('http://layer:8001/resource/', headers = headers)
                        return HttpResponse(third_response.content, status = third_response.status_code)
                    else:
                        return HttpResponse(second_response.content, status = second_response.status_code)

                else:
                    return HttpResponse(first_response.content, status = first_response.status_code)

            else:
                return HttpResponse("[ERROR] - No token found", status = 401)

        else:
            return HttpResponse("[ERROR] - No private key. Are you logged in?", status = 401)
