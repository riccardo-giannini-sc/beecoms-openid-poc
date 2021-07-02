from django.contrib import admin
from django.urls import path, include

from oauth.views import *

urlpatterns = [
    path('', include('frontendapp.urls')),
    path('admin/', admin.site.urls),
    path('oauth/', include('oauth.urls')),
]
