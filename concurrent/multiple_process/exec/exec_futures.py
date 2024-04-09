from concurrent.futures import ThreadPoolExecutor, as_completed


def say_hello_to(name):
    print(name)


def start_future():
    names = ['John', 'Ben', 'Bill', 'Alex', 'Jenny']
    with ThreadPoolExecutor(max_workers=5) as executor:
        for val in names:
            executor.submit(say_hello_to, val)


def say_hello_to_v1(name):
    return f"Hi,{name}"


def start_future_v1():
    names = ['John', 'Ben', 'Bill', 'Alex', 'Jenny']
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for val in names:
            future = executor.submit(say_hello_to_v1, val)
            futures.append(future)
        for future in as_completed(futures):
            print(future.result())

def say_hello_to_v2(name):
    return f"Hi,{name}"


def start_future_v2():
    names = ['John', 'Ben', 'Bill', 'Alex', 'Jenny']
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(say_hello_to_v2, names)
        for r in results:
            print(r)

if __name__ == "__main__":
    start_future_v2()
