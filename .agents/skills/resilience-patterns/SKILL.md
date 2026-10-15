---
name: resilience-patterns
description: Implements production resilience patterns: Circuit Breakers, Retries with Exponential Backoff and Jitter, Timeout Deadlines, Rate Limiting, and Graceful Fallbacks. Use when connecting to external APIs, microservices, or flaky third-party integrations.
---

# Resilience Patterns for Distributed Systems

A field guide for making outbound calls reliable, preventing cascading failures, and absorbing downstream outages gracefully.

---

## 1. Retry with Exponential Backoff and Full Jitter

Never retry immediately in a tight loop. Immediate retries cause **thundering herd** problems that take down recovering services.

### The Full Jitter Formula
$$t = \text{random\_uniform}(0, \min(\text{max\_backoff}, \text{base} \times 2^{\text{attempt}}))$$

```python
import random
import time
import requests

def fetch_with_retry(url: str, max_retries: int = 3, base_delay: float = 0.5, max_delay: float = 10.0):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=3.0)
            if response.status_code < 500: # Do not retry 4xx client errors
                return response
        except (requests.Timeout, requests.ConnectionError) as e:
            if attempt == max_retries - 1:
                raise e

        # Exponential backoff with full jitter
        ceiling = min(max_delay, base_delay * (2 ** attempt))
        sleep_time = random.uniform(0, ceiling)
        time.sleep(sleep_time)

    raise TimeoutError("Max retries exceeded")
```

---

## 2. Circuit Breaker Pattern

Stop sending requests to an endpoint that is already failing.

### State Transitions
- **CLOSED**: Normal operation. Requests flow through. Consecutive failures are counted.
- **OPEN**: Failure threshold breached (e.g. 5 failures in 10s). Requests fail immediately without hitting the network.
- **HALF-OPEN**: Cooldown period elapsed (e.g. 30s). A single canary request is allowed through. If it succeeds, the breaker resets to CLOSED; if it fails, it returns to OPEN.

```python
from enum import Enum
import time

class CircuitState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

class SimpleCircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 30.0):
        self.threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.last_state_change = time.time()

    def can_execute(self) -> bool:
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_state_change > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                return True
            return False
        return True

    def record_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def record_failure(self):
        self.failure_count += 1
        if self.failure_count >= self.threshold:
            self.state = CircuitState.OPEN
            self.last_state_change = time.time()
```

---

## 3. Strict Timeout Budgets

Never make an HTTP or database call without an explicit timeout. A call without a timeout will tie up an execution thread indefinitely if the remote server hangs without closing the socket:

```python
# BAD: Can hang forever
requests.get("https://api.partner.com/data")

# GOOD: Strict connection and read timeout
requests.get("https://api.partner.com/data", timeout=(1.0, 3.0)) # (connect, read)
```

---

## 4. Fallbacks & Degraded Modes

When a non-critical downstream service is down, fall back rather than crashing the user experience:
- **Recommendation service down?** Show top 10 globally popular items from static cache.
- **Avatar service down?** Render SVG initials placeholder.
- **Exchange rate API down?** Use cached rates with a visual "Updated 1h ago" warning.
