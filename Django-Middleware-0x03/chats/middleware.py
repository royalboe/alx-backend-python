# your_app/middleware.py
import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('request_logger')

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.start_time = time(18, 0)  # 6 PM
        self.end_time = time(21, 0)    # 9 PM

    def __call__(self, request):
        # Only apply restriction to chat-related URLs
        if request.path.startswith("/api/onversations/"):
            now = datetime.now().time()
            if not (self.start_time <= now <= self.end_time):
                return HttpResponseForbidden("Access to chat is only allowed between 6 PM and 9 PM.")

        return self.get_response(request)