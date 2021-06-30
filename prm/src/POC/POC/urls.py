from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.urls import path, include
from oauth2_provider.urls import base_urlpatterns, management_urlpatterns, app_name

from decorator_include import decorator_include

def check_superuser():

    return user_passes_test(lambda u: u.is_superuser)


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('m/', decorator_include([user_passes_test(lambda u: u.is_superuser, login_url = '/404/', redirect_field_name = ''), ], (management_urlpatterns, app_name)) ),
    path('o/', include((base_urlpatterns, app_name), namespace = app_name)),
]
