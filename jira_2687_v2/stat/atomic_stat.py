import threading


class StatAtomic:
    def __init__(self):
        self._index = 0
        self._fail_count = 0
        self._success_count = 0
        self.lock = threading.Lock()

    def incr_index(self):
        with self.lock:
            self._index += 1

    def incr_success_count(self):
        with self.lock:
            self._success_count += 1

    def incr_fail_count(self):
        with self.lock:
            self._fail_count += 1

    def get_index(self):
        return self._index

    def get_success_count(self):
        return self._success_count

    def get_fail_count(self):
        return self._fail_count
