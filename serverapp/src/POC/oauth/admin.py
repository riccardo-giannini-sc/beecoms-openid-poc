from django.contrib import admin
from .models import *

@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    pass

@admin.register(AccessToken)
class AccessTokenAdmin(admin.ModelAdmin):
    pass

@admin.register(RefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):
    pass
