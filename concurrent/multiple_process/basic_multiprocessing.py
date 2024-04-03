import os

from multiprocessing import Process


def run_proc(name):
    print(f"子进程运行中,name={name},pid={os.getpid()}...")

if __name__ == "__main__":
    print(f"父进程={os.getpid()}")
    p = Process(target=run_proc, args=('test',))
    print(">>>Start 子进程开始运行")
    p.start();
    p.join();
    print(">>>Start 子进程运行结束")
