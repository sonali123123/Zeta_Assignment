# Python Sliding-Window Rate Limiter

A simple in-memory rate limiter that caps each user at **5 requests per second** using a sliding-window algorithm powered by a `collections.deque`. Ideal for lightweight services or prototypes.


## Features

- **Per-user limits**: Tracks requests independently for each user ID.  
- **Sliding-window**: Always enforces up to _N_ requests in the last _T_ seconds.  
- **O(1) operations**: Uses `deque` for constant-time enqueue/dequeue of timestamps.  
- **Lightweight**: Pure-Python, zero external dependencies.  