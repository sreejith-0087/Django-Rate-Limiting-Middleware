import time
from django.core.cache import cache
from django.http import HttpResponse

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)
        cache_key = f"rate_limit:{ip}"
        request_data = cache.get(cache_key, [])

        current_time = time.time()
        request_data = [t for t in request_data if current_time - t < 300]

        if len(request_data) >= 15:
            return HttpResponse("Too many requests", status=429)

        request_data.append(current_time)
        cache.set(cache_key, request_data, timeout=300)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Extract client IP address."""
        return request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR')).split(',')[0]
