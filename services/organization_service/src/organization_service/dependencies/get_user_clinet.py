"""
This creates ONE instance of the client that's shared across your app.
Think of it as a single telephone that everyone uses, instead of buying a new phone for every call.
"""

from organization_service.http_clients.user_service_client import UserServiceClient

# Global variable to hold the client instance
_user_service_client = None

def get_user_client() -> UserServiceClient:
    """
    Returns the same UserServiceClient instance every time.
    This is called "Singleton Pattern".
    """
    global _user_service_client
    
    if _user_service_client is None:
        print("🆕 Creating new UserServiceClient instance...")
        _user_service_client = UserServiceClient()
    
    return _user_service_client