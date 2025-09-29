import os
from datetime import datetime

class RequestLoggingMiddleware:
    """
    Middleware that logs each user's requests to a file
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Ensure logs directory exists
        os.makedirs('logs', exist_ok=True)
        self.log_file = 'logs/requests.log'
    
    def __call__(self, request):
        # Process the request
        response = self.get_response(request)
        
        # Log the request information
        user = request.user if request.user.is_authenticated else 'Anonymous'
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = f"{timestamp} - User: {user} - Path: {request.path} - Method: {request.method} - Status: {response.status_code}\n"
        
        # Write to log file
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
        
        return response
      import time
from django.http import HttpResponseForbidden
from collections import defaultdict

class RateLimitMiddleware:
    """
    Middleware that limits the number of chat messages a user can send 
    within a certain time window based on their IP address
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Store request counts per IP: {ip: [(timestamp, count), ...]}
        self.request_counts = defaultdict(list)
        self.limit = 5  # 5 messages per minute
        self.window = 60  # 1 minute window
    
    def __call__(self, request):
        # Only apply rate limiting to POST requests for messages
        if request.method == 'POST' and any(path in request.path for path in ['/api/messages/', '/chats/']):
            # Get client IP address
            ip = self.get_client_ip(request)
            current_time = time.time()
            
            # Clean old entries outside the time window
            self.clean_old_entries(ip, current_time)
            
            # Check if user has exceeded the rate limit
            if len(self.request_counts[ip]) >= self.limit:
                return HttpResponseForbidden(
                    "Rate limit exceeded. Please wait before sending more messages."
                )
            
            # Add current request to the count
            self.request_counts[ip].append(current_time)
        
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
    
    def clean_old_entries(self, ip, current_time):
        """Remove entries older than the time window"""
        self.request_counts[ip] = [
            timestamp for timestamp in self.request_counts[ip] 
            if current_time - timestamp < self.window
      ] from django.http import HttpResponseForbidden
from django.contrib.auth.models import User

class RolePermissionMiddleware:
    """
    Middleware that checks user's role before allowing access to specific actions
    Only admin or moderator users can access certain endpoints
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Define protected paths that require admin/moderator access
        self.protected_paths = [
            '/api/admin/',
            '/api/users/',
            '/api/reports/',
        ]
    
    def __call__(self, request):
        # Check if the request path requires special permissions
        requires_permission = any(request.path.startswith(path) for path in self.protected_paths)
        
        if requires_permission:
            # Check if user is authenticated and has admin/moderator role
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required.")
            
            # Check user role (assuming we have a way to determine roles)
            if not self.has_admin_permission(request.user):
                return HttpResponseForbidden("Insufficient permissions. Admin or moderator role required.")
        
        response = self.get_response(request)
        return response
    
    def has_admin_permission(self, user):
        """
        Check if user has admin or moderator permissions
        This can be extended based on your user model structure
        """
        # For simplicity, using is_staff or is_superuser as admin indicator
        # In a real app, you might have a proper role system
        return user.is_staff or user.is_superuser or hasattr(user, 'is_moderator') and user.is_moderator
      import os
import time
from datetime import datetime
from collections import defaultdict
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User

class RequestLoggingMiddleware:
    """
    Middleware that logs each user's requests to a file
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Ensure logs directory exists
        os.makedirs('logs', exist_ok=True)
        self.log_file = 'logs/requests.log'
    
    def __call__(self, request):
        # Process the request
        response = self.get_response(request)
        
        # Log the request information
        user = request.user if request.user.is_authenticated else 'Anonymous'
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = f"{timestamp} - User: {user} - Path: {request.path} - Method: {request.method} - Status: {response.status_code}\n"
        
        # Write to log file
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
        
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to the messaging app during certain hours
    Blocks access between 9 PM (21:00) and 6 AM (06:00)
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        current_hour = datetime.now().hour
        
        # Check if current time is between 9 PM (21) and 6 AM (6)
        if current_hour >= 21 or current_hour < 6:
            # Check if the request is for chat-related endpoints
            if any(path in request.path for path in ['/api/conversations/', '/api/messages/', '/chats/']):
                return HttpResponseForbidden(
                    "Chat access is restricted between 9 PM and 6 AM. Please try again during allowed hours."
                )
        
        response = self.get_response(request)
        return response


class RateLimitMiddleware:
    """
    Middleware that limits the number of chat messages a user can send 
    within a certain time window based on their IP address
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Store request counts per IP: {ip: [(timestamp, count), ...]}
        self.request_counts = defaultdict(list)
        self.limit = 5  # 5 messages per minute
        self.window = 60  # 1 minute window
    
    def __call__(self, request):
        # Only apply rate limiting to POST requests for messages
        if request.method == 'POST' and any(path in request.path for path in ['/api/messages/', '/chats/']):
            # Get client IP address
            ip = self.get_client_ip(request)
            current_time = time.time()
            
            # Clean old entries outside the time window
            self.clean_old_entries(ip, current_time)
            
            # Check if user has exceeded the rate limit
            if len(self.request_counts[ip]) >= self.limit:
                return HttpResponseForbidden(
                    "Rate limit exceeded. Please wait before sending more messages."
                )
            
            # Add current request to the count
            self.request_counts[ip].append(current_time)
        
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
    
    def clean_old_entries(self, ip, current_time):
        """Remove entries older than the time window"""
        self.request_counts[ip] = [
            timestamp for timestamp in self.request_counts[ip] 
            if current_time - timestamp < self.window
        ]


class RolePermissionMiddleware:
    """
    Middleware that checks user's role before allowing access to specific actions
    Only admin or moderator users can access certain endpoints
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Define protected paths that require admin/moderator access
        self.protected_paths = [
            '/api/admin/',
            '/api/users/',
            '/api/reports/',
        ]
    
    def __call__(self, request):
        # Check if the request path requires special permissions
        requires_permission = any(request.path.startswith(path) for path in self.protected_paths)
        
        if requires_permission:
            # Check if user is authenticated and has admin/moderator role
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required.")
            
            # Check user role (assuming we have a way to determine roles)
            if not self.has_admin_permission(request.user):
                return HttpResponseForbidden("Insufficient permissions. Admin or moderator role required.")
        
        response = self.get_response(request)
        return response
    
    def has_admin_permission(self, user):
        """
        Check if user has admin or moderator permissions
        This can be extended based on your user model structure
        """
        # For simplicity, using is_staff or is_superuser as admin indicator
        # In a real app, you might have a proper role system
        return user.is_staff or user.is_superuser or hasattr(user, 'is_moderator') and user.is_moderator
