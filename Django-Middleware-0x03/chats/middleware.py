import datetime
import logging
from django.utils import timezone
from django.http import HttpResponseForbidden, JsonResponse
from django.core.cache import cache
import re

# Setup logging for request logging
logger = logging.getLogger('request_logger')
file_handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    """
    Middleware to log each user's requests including timestamp, user and request path
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get user information
        user = "Anonymous"
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user.username
        
        # Log the request
        log_message = f"User: {user} - Path: {request.path}"
        logger.info(log_message)
        
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to the messaging app during certain hours (9PM to 6AM)
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = timezone.now().time()
        start_time = datetime.time(21, 0)  # 9 PM
        end_time = datetime.time(6, 0)     # 6 AM
        
        # Check if current time is between 9PM and 6AM
        if (current_time >= start_time) or (current_time <= end_time):
            # Check if the request is accessing chat-related URLs
            if any(path in request.path for path in ['/chat', '/message', '/api/']):
                return HttpResponseForbidden(
                    "Access denied: Chat service is unavailable from 9 PM to 6 AM"
                )
        
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    """
    Middleware that detects and blocks offensive language in messages
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # List of offensive words to detect
        self.offensive_words = [
            'badword1', 'badword2', 'offensive', 'hate', 'spam'
        ]

    def __call__(self, request):
        # Only check POST requests that might contain messages
        if request.method == 'POST':
            # Check form data
            if hasattr(request, 'POST'):
                for field, value in request.POST.items():
                    if self.contains_offensive_language(str(value)):
                        return JsonResponse({
                            'error': 'Message contains offensive language and cannot be sent'
                        }, status=400)
            
            # Check JSON data for API requests
            if hasattr(request, 'data'):
                if isinstance(request.data, dict):
                    for key, value in request.data.items():
                        if self.contains_offensive_language(str(value)):
                            return JsonResponse({
                                'error': 'Message contains offensive language and cannot be sent'
                            }, status=400)
        
        response = self.get_response(request)
        return response
    
    def contains_offensive_language(self, text):
        """Check if text contains any offensive words"""
        text_lower = text.lower()
        for word in self.offensive_words:
            if word in text_lower:
                return True
        return False


class RateLimitMiddleware:
    """
    Middleware that limits the number of chat messages a user can send within a time window
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.limit = 5  # 5 messages
        self.window = 60  # 1 minute in seconds

    def __call__(self, request):
        # Only apply rate limiting to POST requests for messages
        if request.method == 'POST' and any(path in request.path for path in ['/message', '/chat']):
            # Get client IP address
            ip_address = self.get_client_ip(request)
            cache_key = f"rate_limit_{ip_address}"
            
            # Get current count from cache
            current_count = cache.get(cache_key, 0)
            
            if current_count >= self.limit:
                return JsonResponse({
                    'error': f'Rate limit exceeded. Maximum {self.limit} messages per minute.'
                }, status=429)
            
            # Increment count
            cache.set(cache_key, current_count + 1, self.window)
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Extract client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolePermissionMiddleware:
    """
    Middleware that checks user's role before allowing access to specific actions
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define admin-only paths and actions
        admin_paths = ['/admin/', '/delete/', '/moderate/']
        admin_actions = ['delete', 'moderate', 'ban']
        
        # Check if request is accessing admin-only functionality
        is_admin_path = any(path in request.path for path in admin_paths)
        is_admin_action = any(action in request.path for action in admin_actions)
        
        if is_admin_path or is_admin_action:
            # Check if user is authenticated and has admin/mod role
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required")
            
            # Check user role (assuming you have a role field or is_staff/is_superuser)
            if not (request.user.is_staff or request.user.is_superuser or 
                   hasattr(request.user, 'role') and request.user.role in ['admin', 'moderator']):
                return HttpResponseForbidden("Insufficient permissions. Admin or moderator role required.")
        
        response = self.get_response(request)
        return response
