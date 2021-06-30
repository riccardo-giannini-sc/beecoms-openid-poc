from django.db import models
from django.contrib.auth.models import User

class AppUser(User):
    salt = models.CharField(max_length = 32, null = True, blank = True, verbose_name = "Salt")

class AccessToken(models.Model):
    user = models.ForeignKey(AppUser, on_delete = models.CASCADE)
    token = models.CharField(max_length=255)
    expires = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    scope = models.TextField(blank=True)

class RefreshToken(models.Model):
    user = models.ForeignKey(AppUser, on_delete = models.CASCADE)
    token = models.CharField(max_length=255)
    access_token = models.ForeignKey(AccessToken, on_delete = models.SET_NULL, blank = True, null = True)
    revoked = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
