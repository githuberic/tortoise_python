from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def draw(self):
        pass


class Circle(Shape):
    def draw(self):
        return "Drawing Circle"


class Square(Shape):
    def draw(self):
        return "Drawing Square"


# 多态性的体现
def draw_shape(shape):
    print(shape.draw())


def start():
    shapes = [Circle(), Square()]
    for shape in shapes:
        draw_shape(shape)


if __name__ == "__main__":
    start()
