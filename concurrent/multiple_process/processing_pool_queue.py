import os
from multiprocessing import Manager, Pool


def write(q):
    print(f"Write进程{os.getpid()}开始执行,父进程={os.getppid()}")
    for val in ['A', 'B', 'C', 'D', 'E', 'F']:
        q.put(val)


def read(q):
    print(f"Read进程{os.getpid()}开始执行,父进程={os.getppid()}")
    while True:
        if not q.empty():
            val = q.get(True)
            print(f"Get {val} from queue")
        else:
            break


if __name__ == '__main__':
    q = Manager().Queue()
    po = Pool()
    po.apply_async(write, (q,))
    po.apply_async(read, (q,))
    po.close()
    po.join()
    print(f">>> {os.getpid()}Done")
