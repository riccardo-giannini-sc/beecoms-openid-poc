from oauth2_provider.views.mixins import OAuthLibMixin
from django.views.generic import View
from django.http import HttpResponseForbidden, JsonResponse
import json

class ExtendedProtectedResourceMixin(OAuthLibMixin):
    def dispatch(self, request, *args, **kwargs):
        # let preflight OPTIONS requests pass
        if request.method.upper() == "OPTIONS":
            return super().dispatch(request, *args, **kwargs)

        # check if the request is valid and the protected resource may be accessed
        valid, r = self.verify_request(request)
        if valid:
            request.resource_owner = r.user
            return super().dispatch(request, *args, **kwargs)
        else:
            if hasattr(r, 'oauth2_error') and (r.oauth2_error['error'] == 'invalid_token'):
                description = r.oauth2_error['error_description']
                data = {'error': description}
                return JsonResponse(data, status = 401)
            else:
                return HttpResponseForbidden()


class ExtendedProtectedResourceView(ExtendedProtectedResourceMixin, OAuthLibMixin, View):
    pass
