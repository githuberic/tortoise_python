class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age

    def prt_self(this):
        print(this)
        print(this.__class__)

    def GetUserInfo(self):
        return "{}的年龄为{}".format(self._name, self._age)

    def __str__(self):
        return "{}的年龄为{}".format(self._name, self._age)

    def setAge(self, age):
        if 0 < age < 120:
            self._age = age


def start():
    person = Person('lgq', 18)
    person.prt_self()
    print(person.GetUserInfo())

    print(person.setAge(19))
    print(person.GetUserInfo())


if __name__ == "__main__":
    start()
