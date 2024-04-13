class Vehicle:
    def drive(self):
        raise NotImplementedError


# 多态重写
class Car(Vehicle):
    def drive(self):
        print("驾驶汽车...")


class Bicycle(Vehicle):
    def drive(self):
        print("骑自行车...")


def start():
    car = Car()
    bicycle = Bicycle()

    vehicle = [car, bicycle]
    for vehi in vehicle:
        vehi.drive()


if __name__ == "__main__":
    start()
