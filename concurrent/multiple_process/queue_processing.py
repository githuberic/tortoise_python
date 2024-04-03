import os
import random
import time
from multiprocessing import Manager, Process, Queue


def write(q):
    for val in ['A', 'B', 'C']:
        print(f"Put{val} to queue...")
        q.put(val)
        time.sleep(random.random())


def read(q):
    while True:
        if not q.empty():
            val = q.get(True)
            print(f"Get {val} from queue...")
            time.sleep(random.random())
        else:
            break


if __name__ == '__main__':
    q = Manager().Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    pw.start()
    pw.join()
    pr.start()
    pr.join()
    print(">>>Done")
