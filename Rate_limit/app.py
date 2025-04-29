import time
from collections import defaultdict, deque

class RateLimiter:
    def __init__(self, max_requests: int, period: float):
        
        self.max_requests = max_requests
        self.period = period
        # Maps user_id to a deque of request timestamps
        self.requests = defaultdict(deque)

    def allow_request(self, user_id: str) -> bool:
        """
        Returns True if the request is allowed, False if rate limit exceeded.
        """
        now = time.time()
        q = self.requests[user_id]

        # Discard timestamps older than the sliding window
        while q and q[0] <= now - self.period:
            q.popleft()

        if len(q) < self.max_requests:
            q.append(now)
            return True
        else:
            return False

if __name__ == "__main__":
    rl = RateLimiter(max_requests=5, period=1.0)  # 5 requests per 1 second window
    user = "alice"

    # simulate 7 quick requests
    for i in range(7):
        allowed = rl.allow_request(user)
        print(f"Request {i+1} for {user}: {'Allowed' if allowed else 'Denied'}")
        # no sleep → all timestamps within 1 second
