import threading


class Counter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.count += 1

    def decrement(self):
        with self.lock:
            self.count -= 1

    def get_count(self):
        return self.count


def worker(counter, operation, times):
    for _ in range(times):
        if operation == "increment":
            counter.increment()
        elif operation == "decrement":
            counter.decrement()


if __name__ == '__main__':
    counter = Counter()
    threads = []

    for _ in range(10):
        t1 = threading.Thread(target=worker, args=(counter, "increment", 1000))
        t2 = threading.Thread(target=worker, args=(counter, "decrement", 300))
        threads.append(t1)
        threads.append(t2)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(f"最终计数值: {counter.get_count()}")
