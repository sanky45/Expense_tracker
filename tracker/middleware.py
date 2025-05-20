import re
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]

    def __call__(self, request):
        if not request.user.is_authenticated:
            if not any(url.match(request.path) for url in self.exempt_urls):
                return redirect(reverse('login'))
        response = self.get_response(request)
        return response