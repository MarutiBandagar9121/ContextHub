import httpx
import logging
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

# Setup logging - so we can see what's happening
logger = logging.getLogger(__name__)

class BaseHTTPClient:
    """
    This is the "Swiss Army Knife" for all HTTP calls.
    Every other client (User, Product, etc.) will use this.
    """
    
    def __init__(self, base_url: str, timeout: int = 30):
        """
        Initialize with the service URL
        
        Args:
            base_url: The URL of the service (e.g., http://localhost:8080)
            timeout: How long to wait before giving up (seconds)
        """
        self.base_url = base_url.rstrip('/')  # Remove trailing slash if any
        self.timeout = timeout
        self.client = None  # Will hold the actual HTTP client
    
    async def __aenter__(self):
        """
        This is called when you do: async with BaseHTTPClient(...) as client:
        It creates the HTTP connection
        """
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={"User-Agent": "org-service"}  # Identify ourselves
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        This is called when the 'with' block ends.
        It closes the HTTP connection to prevent resource leaks
        """
        if self.client:
            await self.client.aclose()
    
    @retry(
        # Try this many times
        stop=stop_after_attempt(3),
        # Wait between retries: 1s, 2s, 4s, etc. (exponential backoff)
        wait=wait_exponential(multiplier=1, min=1, max=10),
        # Only retry on these types of errors
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError))
    )
    async def _make_request(self, method: str, endpoint: str, **kwargs):
        """
        INTERNAL METHOD: Makes the actual HTTP request with retry logic
        
        This is where the magic happens:
        1. If request fails due to timeout/network, it retries
        2. Logs everything
        3. Raises helpful errors
        """
        if not self.client:
            raise RuntimeError("Client not initialized. Use 'async with' context manager.")
        
        try:
            # Make the request
            response = await self.client.request(method, endpoint, **kwargs)
            
            # If status is 4xx or 5xx, this raises an exception
            response.raise_for_status()
            
            return response
            
        except httpx.HTTPStatusError as e:
            # Handle HTTP errors (404, 500, etc.)
            logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
            raise
            
        except Exception as e:
            # Handle all other errors
            logger.error(f"Request failed: {str(e)}")
            raise
    
    # PUBLIC METHODS - These are what your code will actually use
    
    async def get(self, endpoint: str, params=None, **kwargs):
        """Make a GET request"""
        return await self._make_request("GET", endpoint, params=params, **kwargs)
    
    async def post(self, endpoint: str, json=None, **kwargs):
        """Make a POST request with JSON body"""
        return await self._make_request("POST", endpoint, json=json, **kwargs)