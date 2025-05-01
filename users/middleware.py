import requests
from django.shortcuts import redirect

class LocationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.profile.city in [None, ""]:
            ip = get_client_ip(request)
            try:
                response = requests.get(f"http://ip-api.com/json/{ip}").json()
                city = response.get("city")
                if city:
                    request.session['detected_city'] = city
            except:
                pass
        return self.get_response(request)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')
