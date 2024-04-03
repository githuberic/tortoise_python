import os


def fun_fork():
    rpid = os.fork()
    if rpid < 0:
        print("调用子进程失败")
    elif rpid == 0:
        print("当前是子进程,子进程=(%s),其父进程=(%s)" % (os.getpid(), os.getppid()))
    else:
        print("当前是父进程,进程=(%s),其子进程=(%s)" % (os.getpid(), rpid))


if __name__ == "__main__":
    fun_fork()
