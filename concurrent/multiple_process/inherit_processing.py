import os
import time
from multiprocessing import Process


class Process_Class(Process):
    def __init__(self, interval):
        Process.__init__(self)
        self.interval = interval

    def run(self):
        print(f"子进程{os.getpid()}开始执行,父进程={os.getppid()}")
        t_start = time.time()
        time.sleep(self.interval)
        t_stop = time.time()
        print(f"{os.getpid()}执行结束,耗时={t_stop - t_start:.2f}秒", )


if __name__ == "__main__":
    t_start = time.time()
    print(f"当前程序进程={os.getpid()}")
    p1 = Process_Class(2)
    p1.start()
    p1.join()
    t_stop = time.time()
    print(f"{os.getpid()}执行结束,耗时={t_stop - t_start:.2f}秒")
