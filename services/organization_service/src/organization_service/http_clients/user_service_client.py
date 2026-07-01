import logging
from typing import List, Dict, Any, Optional

from fastapi import HTTPException, status
from httpx import HTTPStatusError
from pydantic import EmailStr, TypeAdapter, ValidationError

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

        async with BaseHTTPClient(self.base_url, self.timeout) as client:
            try:
                response = await client.post(
                    "/user/batch",
                    json={"user_ids": user_ids}
                )
            except HTTPStatusError as e:
                logger.error(f"user_service error fetching users {user_ids}: {e.response.status_code} {e.response.text}")
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="User service returned an error"
                ) from e

            try:
                users = TypeAdapter(List[UserServiceUserDetailsResponse]).validate_json(response.text)
            except ValidationError as e:
                logger.error(f"User service response validation failed: {e}")
                logger.error(f"Response: {response.text[:500]}")
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="User service returned malformed data"
                ) from e

            logger.info(f"Successfully fetched {len(users)} users")
            return users

    async def get_user_by_email(self, email: EmailStr) -> UserServiceUserDetailsResponse:
        async with BaseHTTPClient(self.base_url, self.timeout) as client:
            try:
                response = await client.get(
                    "/user",
                    params={"email": email}
                )
            except HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User with email '{email}' not found"
                    ) from e
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="User service returned an error"
                ) from e

            try:
                return UserServiceUserDetailsResponse.model_validate_json(response.text)
            except ValidationError as e:
                logger.error(f"User service response validation failed: {e}")
                logger.error(f"Response: {response.text[:500]}")
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="User service returned malformed data"
                ) from e