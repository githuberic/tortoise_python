class Person:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    def GetUserInfo(self):
        return "{}的年龄为{}".format(self.__name, self.__age)

    def __str__(self):
        return "{}的年龄为{}".format(self.__name, self.__age)

    def setAge(self, age):
        if 0 < age < 120:
            self.__age = age


def start():
    person = Person('lgq', 18)
    print(person.GetUserInfo())

    print(person.setAge(19))
    print(person.GetUserInfo())


if __name__ == "__main__":
    start()
