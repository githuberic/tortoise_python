###
## 进程池执行器
###
from concurrent.futures import ProcessPoolExecutor


def say_hello_to(name):
    return f"Hi,{name}"


def start_future():
    names = ['John', 'Ben', 'Bill', 'Alex', 'Jenny']
    with ProcessPoolExecutor(max_workers=5) as executor:
        results = executor.map(say_hello_to, names)
        for val in results:
            print(val)


if __name__ == "__main__":
    start_future()
