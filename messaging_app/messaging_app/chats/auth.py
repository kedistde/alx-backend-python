from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class that provides additional validation
    and user context for the messaging app.
    """
    
    def authenticate(self, request):
        """
        Override the authenticate method to add custom validation
        """
        try:
            # Get the header and validate
            header = self.get_header(request)
            if header is None:
                return None

            # Get the raw token
            raw_token = self.get_raw_token(header)
            if raw_token is None:
                return None

            # Validate the token and get the user
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
            
            # Additional custom validation can be added here
            # For example, check if user is active
            if not user.is_active:
                raise AuthenticationFailed('User is inactive', code='user_inactive')
            
            return (user, validated_token)
            
        except AuthenticationFailed:
            # Re-raise authentication failures
            raise
        except Exception as e:
            # Handle any other exceptions
            raise AuthenticationFailed('Authentication failed', code='authentication_failed')

class OptionalJWTAuthentication(JWTAuthentication):
    """
    Optional JWT authentication that doesn't raise errors if token is invalid.
    Useful for endpoints that can work with both authenticated and unauthenticated users.
    """
    
    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except Exception:
            # Return None if authentication fails, allowing other auth methods to try
            return None

class SafeSessionAuthentication(SessionAuthentication):
    """
    Custom session authentication that handles CSRF tokens safely
    for API requests.
    """
    
    def authenticate(self, request):
        """
        Override to handle CSRF more gracefully for API clients
        """
        try:
            return super().authenticate(request)
        except Exception:
            # Return None if session auth fails
            return None
