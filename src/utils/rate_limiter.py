"""Rate limiter to avoid overwhelming LinkedIn servers"""
import time
from collections import deque
from typing import Optional


class RateLimiter:
    """Simple rate limiter using sliding window algorithm"""

    def __init__(self, max_requests: int = 10, time_window: int = 60):
        """
        Initialize rate limiter

        Args:
            max_requests: Maximum number of requests allowed
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: deque = deque()

    def wait_if_needed(self) -> Optional[float]:
        """
        Wait if rate limit is reached

        Returns:
            Sleep time in seconds if wait was needed, None otherwise
        """
        now = time.time()

        # Remove old requests outside the time window
        while self.requests and self.requests[0] < now - self.time_window:
            self.requests.popleft()

        # Check if we've hit the limit
        if len(self.requests) >= self.max_requests:
            # Calculate sleep time
            oldest_request = self.requests[0]
            sleep_time = (oldest_request + self.time_window) - now

            if sleep_time > 0:
                time.sleep(sleep_time)
                return sleep_time

        # Record this request
        self.requests.append(now)
        return None

    def reset(self):
        """Reset the rate limiter"""
        self.requests.clear()
