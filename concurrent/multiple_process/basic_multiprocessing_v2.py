import os
from multiprocessing import Process
from time import sleep


def run_proc(name, age, **kwargs):
    for i in range(10):
        print(f"子进程运行中,name={name},age={age},pid={os.getpid()}...")
        print(kwargs)
        sleep(0.5)


if __name__ == "__main__":
    print(f"父进程={os.getpid()}")
    p = Process(target=run_proc, args=('test', 28), kwargs={"m": 19})
    print(">>>Start 子进程开始运行")
    p.start()
    sleep(1)
    p.terminate()
    p.join()
    print(">>>Start 子进程运行结束")
