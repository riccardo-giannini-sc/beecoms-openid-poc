import datetime
import secrets
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

import os
import json
from django.conf import settings

from .models import AccessToken, RefreshToken


def store_access_token(access_token, app_user_obj, expires, scope, current_privkey):
    f = Fernet(current_privkey)
    protected_access_token = f.encrypt(access_token.encode())
    access_token_obj = AccessToken.objects.create(
         user = app_user_obj,
         token = protected_access_token,
         expires = datetime.datetime.now() + datetime.timedelta(0, expires),
         scope = scope
    )
    return access_token_obj

def store_refresh_token(refresh_token, app_user_obj, access_token_obj, current_privkey):
    f = Fernet(current_privkey)
    protected_refresh_token = f.encrypt(refresh_token.encode())
    refresh_token_obj = RefreshToken.objects.create(
         user = app_user_obj,
         token = protected_refresh_token,
         access_token = access_token_obj,
    )
    return refresh_token_obj

def build_refresh_token_request(app_user_obj, f):
    with open(os.path.join(settings.BASE_DIR, 'POC/secrets.json')) as client_info:
        data = json.loads(client_info.read())
        client_id = data["client_id"]
        client_secret = data["client_secret"]

    refresh_token_obj = RefreshToken.objects.filter(user = app_user_obj).last()
    refresh_token = f.decrypt(refresh_token_obj.token).decode('utf-8')

    post_data = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token
    }
    post_headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    return post_data, post_headers
