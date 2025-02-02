from django.test import TestCase, RequestFactory
from django.core.cache import cache
from .middleware import RateLimitMiddleware
from unittest.mock import Mock
import time

class RateLimitMiddlewareTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.get_response = Mock(return_value=None)
        self.middleware = RateLimitMiddleware(get_response=self.get_response)
        self.cache_key = "rate_limit:192.168.1.1"
        cache.clear()

    def test_rate_limit_allowed(self):
        for i in range(14):
            request = self.factory.get('/')
            request.META['REMOTE_ADDR'] = '192.168.1.1'
            self.middleware.__call__(request)
        request = self.factory.get('/')
        request.META['REMOTE_ADDR'] = '192.168.1.1'
        response = self.middleware.__call__(request)

        self.assertIsNone(response)

    def test_rate_limit_exceeded(self):
        for i in range(15):
            request = self.factory.get('/')
            request.META['REMOTE_ADDR'] = '192.168.1.1'
            self.middleware.__call__(request)
        request = self.factory.get('/')
        request.META['REMOTE_ADDR'] = '192.168.1.1'
        response = self.middleware.__call__(request)

        self.assertEqual(response.status_code, 429)
        self.assertEqual(response.content.decode(), "Too many requests")

    def test_rate_limit_resets_after_5_minutes(self):
        for i in range(15):
            request = self.factory.get('/')
            request.META['REMOTE_ADDR'] = '192.168.1.1'
            self.middleware.__call__(request)

        time.sleep(300)

        request = self.factory.get('/')
        request.META['REMOTE_ADDR'] = '192.168.1.1'
        response = self.middleware.__call__(request)
        self.assertIsNone(response)
