# your_app/middleware.py
import logging
from datetime import datetime, time, timedelta
from django.http import HttpResponseForbidden, JsonResponse

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
    

from collections import defaultdict

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_log = defaultdict(list)  # {ip: [datetime, datetime, ...]}
        self.limit = 5  # messages
        self.window = timedelta(minutes=1)

    def __call__(self, request):
        # Only apply to chat message creation (assume POST to /api/messages/)
        if request.path.startswith('/api/messages/') and request.method == 'POST':
            ip = self.get_ip(request)
            now = datetime.now()

            # Filter out timestamps older than 1 minute
            self.request_log[ip] = [ts for ts in self.request_log[ip] if now - ts < self.window]

            if len(self.request_log[ip]) >= self.limit:
                return JsonResponse(
                    {"error": "Rate limit exceeded. You can only send 5 messages per minute."},
                    status=429
                )

            # Log current request timestamp
            self.request_log[ip].append(now)

        return self.get_response(request)

    def get_ip(self, request):
        # Use HTTP_X_FORWARDED_FOR if behind a proxy
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')
    

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define the protected paths (you can change this as needed)
        self.protected_paths = [
            "/api/messages/delete/",
            "/api/users/manage/",
            "/api/moderation/"
        ]

    def __call__(self, request):
        # Only check protected paths
        for path in self.protected_paths:
            if request.path.startswith(path):
                if not request.user.is_authenticated:
                    return JsonResponse(
                        {"error": "Authentication required."},
                        status=403
                    )
                # Check user role
                role = getattr(request.user, 'role', None)
                if role not in ['admin', 'moderator']:
                    return JsonResponse(
                        {"error": "You do not have permission to perform this action."},
                        status=403
                    )
                break  # No need to continue checking paths

        return self.get_response(request)
