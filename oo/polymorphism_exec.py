class Shape:
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
    return shape.draw()


def start():
    circle = Circle()
    square = Square()
    print(draw_shape(circle))  # 输出: Drawing Circle
    print(draw_shape(square))  # 输出: Drawing Square


if __name__ == "__main__":
    start()
