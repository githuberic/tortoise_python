import types


class Animal:
    def __init__(self):
        pass


def run(self):
    print('Running>>>')

def info():
    print('Info>>>')


def start():
    cat = Animal()
    cat.run = types.MethodType(run, cat)
    cat.run()

    Animal.color = 'Red'
    print(cat.color)

    Animal.info = info
    Animal.info()


if __name__ == "__main__":
    start()
