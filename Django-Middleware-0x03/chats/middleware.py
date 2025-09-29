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
        timestamp = datetime.now().strftime("%Y-%m-%
