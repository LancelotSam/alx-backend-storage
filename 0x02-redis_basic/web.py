#!/usr/bin/env python3
""" Expiring web cache module """

import redis
import requests
from typing import Callable
from functools import wraps

# Create a Redis instance
redis_client = redis.Redis(host='localhost', port=6379, db=0)


def wrap_requests(fn: Callable) -> Callable:
    """Decorator wrapper to cache requests and count accesses"""

    @wraps(fn)
    def wrapper(url: str) -> str:
        """Wrapper for decorator function"""
        # Increment the access count
        redis_client.incr(f"count:{url}")
        
        # Try to get the cached response
        cached_response = redis_client.get(f"cached:{url}")
        
        if cached_response:
            return cached_response.decode('utf-8')
        
        # Call the original function to get the result
        result = fn(url)
        
        # Cache the result with a TTL of 10 seconds
        redis_client.setex(f"cached:{url}", 10, result)
        
        return result

    return wrapper


@wrap_requests
def get_page(url: str) -> str:
    """Fetches a web page and returns its content"""
    response = requests.get(url)
    return response.text
