class RequestStat2AmazonPD:
    def __init__(self, asin, cookie):
        self.self = self
        self.asin = asin
        self.cookie = cookie
        self._retry_times = 0
        self._cookie_used_times = 0

    def incr_retry_times(self):
        self._retry_times += 1

    def incr_cookie_used_times(self):
        self._cookie_used_times += 1

    def get_retry_times(self):
        return self._retry_times

    def get_retry_times(self):
        return self._retry_times

    def get_cookie_used_times(self):
        return self._cookie_used_times
