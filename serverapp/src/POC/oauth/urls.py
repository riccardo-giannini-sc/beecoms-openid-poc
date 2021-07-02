from django.urls import path, include
from .views import *

urlpatterns = [
    path('login/', login.as_view()),
    path('logout/', logout.as_view()),
    path('client_id/', client_id.as_view()),
    path('authcode/', auth_code.as_view()),
    path('prm_resource/', prm_resource.as_view()),
]
