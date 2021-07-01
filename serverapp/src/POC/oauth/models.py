from django.db import models
from django.contrib.auth.models import User

class AppUser(User):
    salt = models.BinaryField(max_length = 32, null = True, blank = True, verbose_name = "Salt")

class AccessToken(models.Model):
    user = models.ForeignKey(AppUser, on_delete = models.CASCADE)
    token = models.BinaryField()
    expires = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    scope = models.TextField(blank=True)

    def __str__(self):
        return "Access Token " + str(self.id)

class RefreshToken(models.Model):
    user = models.ForeignKey(AppUser, on_delete = models.CASCADE)
    token = models.BinaryField()
    access_token = models.ForeignKey(AccessToken, on_delete = models.SET_NULL, blank = True, null = True)
    revoked = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return "Refresh Token " + str(self.id)
