class A(object):
    def __init__(self, name=None, age=None):
        self._name = name
        self._age = age

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, new_value):
        self._age = new_value

    # age = property(__eat, run)


def start():
    b = A()
    print(b.age)  ## 报错
    b.age = 19
    print(b.age)  ## 报错


if __name__ == "__main__":
    start()
