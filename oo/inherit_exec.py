class Car():
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def __str__(self):
        return f"汽车信息：\n  品牌：{self.make}\n  型号：{self.model}\n  年份：{self.year}"

    def start(self):
        print(f"{self.make} {self.model} 已启动！")


# 继承Car
class ElectricCar(Car):
    def __init__(self, make, model, year, range):
        super().__init__(make, model, year)
        self.range = range

    def __str__(self):
        return f"{super().__str__()}\n  续航里程：{self.range}公里"


if __name__ == "__main__":
    electric_car = ElectricCar("Tesla", "Model 3", 2024, 600)
    print(electric_car)
