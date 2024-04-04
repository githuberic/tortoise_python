import os
from multiprocessing import Lock
from threading import Thread

g_num = 0


def fun_a():
    global g_num
    for i in range(100000):
        metux_flag = mutex.acquire(True)
        if metux_flag:
            g_num += 1
            mutex.release()
    print(f"进程{os.getpid()}--fun_a() 开始执行,g_num={g_num}")


def fun_b():
    global g_num
    for i in range(100000):
        metux_flag = mutex.acquire(True)
        if metux_flag:
            g_num += 1
            mutex.release()
    print(f"进程{os.getpid()}--fun_b() 开始执行,g_num={g_num}")


if __name__ == "__main__":
    mutex = Lock()

    p1 = Thread(target=fun_a)
    p1.start()
    p1.join()

    p2 = Thread(target=fun_b)
    p2.start()
    p2.join()

    print(f">>> {os.getpid()} executed")
