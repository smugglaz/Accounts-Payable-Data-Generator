import time

class RateLimiter:
    def __init__(self, max_per_second):
        self.max_per_second = max_per_second
        self.allowance = max_per_second
        self.last_check = time.time()

    def limit(self):
        current = time.time()
        time_passed = current - self.last_check
        self.last_check = current
        self.allowance += time_passed * self.max_per_second
        if self.allowance > self.max_per_second:
            self.allowance = self.max_per_second
        if self.allowance < 1.0:
            time.sleep((1.0 - self.allowance) / self.max_per_second)
        else:
            self.allowance -= 1.0