import logging
from typing import List, Dict, Any, Optional

from organization_service.config.settings import settings
from organization_service.http_clients.base_client import BaseHTTPClient
from organization_service.schemas.user_schema import UserServiceUserDetailsResponse

logger = logging.getLogger(__name__)

class UserServiceClient:
    """
    This client knows how to talk to the User Service API.
    It uses the BaseHTTPClient for all the heavy lifting.
    """
    
    def __init__(self):
        # Get settings from your config
        self.base_url = settings.user_service_host
        self.timeout = settings.user_service_timeout
        self.service_name = settings.user_service_name
        
        logger.info(f"Initialized UserServiceClient for {self.service_name} at {self.base_url}")
    
    async def get_users_by_ids(self, user_ids: List[int]) -> List[UserServiceUserDetailsResponse]:
        """
        Fetch multiple users by their IDs
        
        Args:
            user_ids: List of user IDs like [1, 2, 3]
            
        Returns:
            List of UserDetails
        """
        if not user_ids:
            logger.info("No user IDs provided, returning empty list")
            return []
        
        # Use the base client to make the request
        async with BaseHTTPClient(self.base_url, self.timeout) as client:
            try:
                # POST request to /user/batch with user_ids in body
                # (You'll need to adjust this endpoint based on your user service)
                response = await client.post(
                    "/user/batch",  # This should match your user service endpoint
                    json={"user_ids": user_ids}
                )
                
                data = response.json()
                
                # Extract users from response
                users_data = data.get("users", []) if isinstance(data, dict) else data

                # Convert to Pydantic models
                user_models = []
                for user_dict in users_data:
                    # Handle different possible response structures
                    # If your user service returns user_id instead of id
                    if "user_id" in user_dict and "id" not in user_dict:
                        user_dict["id"] = user_dict["user_id"]
                    
                    user_models.append(UserServiceUserDetailsResponse(**user_dict))
                
                logger.info(f"✅ Successfully fetched {len(user_models)} users")
                return user_models
                
            except Exception as e:
                logger.error(f"❌ Failed to fetch users: {str(e)}")
                # Re-raise or handle based on your needs
                raise
    
    async def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetch a single user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User dictionary or None if not found
        """
        async with BaseHTTPClient(self.base_url, self.timeout) as client:
            try:
                response = await client.get(f"/users/{user_id}")
                return response.json()
                
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    logger.warning(f"User {user_id} not found")
                    return None
                raise
    
    # Helper method - a shortcut to get only emails
    async def get_user_emails(self, user_ids: List[int]) -> Dict[int, str]:
        """
        Get only email addresses for users
        
        Returns:
            Dict mapping user_id to email: {1: "alice@email.com", 2: "bob@email.com"}
        """
        users = await self.get_users_by_ids(user_ids)
        return {user["id"]: user["email"] for user in users if "email" in user}