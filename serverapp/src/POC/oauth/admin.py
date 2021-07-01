from django.contrib import admin
from .models import *

@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'salt')
    readonly_fields = ('salt', )


@admin.register(AccessToken)
class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ('pk', 'token', 'user', 'expires')
    readonly_fields = ('token', )

@admin.register(RefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):
    list_display = ('pk', 'token', 'user', 'access_token', 'access_token_value')
    readonly_fields = ('token', )

    def access_token_value(self, obj):
        return obj.access_token.token
