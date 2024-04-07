from queue import Queue


def basic():
    q = Queue()
    for i in range(3):
        q.put(i)

    while not q.empty():
        print(q.get())


if __name__ == "__main__":
    basic()
