import datetime
import secrets
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

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
