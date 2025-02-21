import time
from django.conf import settings
from django.contrib.auth import logout
from django.utils.timezone import now

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        last_activity = request.session.get("last_activity")

        if (last_activity
                and (now() - last_activity).seconds > settings.SESSION_COOKIE_AGE):
            logout(request)
        else:
            request.session["last_activity"] = now()

        response = self.get_response(request)
        return response
