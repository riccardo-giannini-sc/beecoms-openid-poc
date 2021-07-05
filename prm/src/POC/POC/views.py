from django.views.generic import View
from django.http import HttpResponse

from oauth2_provider.views.generic import ProtectedResourceView
from .oauth2_ext_views import ExtendedProtectedResourceView

class protectedResource(ExtendedProtectedResourceView):
    def dispatch(self, *args, **kwargs):
        return super(protectedResource, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponse("Simple HTTP response\n")
