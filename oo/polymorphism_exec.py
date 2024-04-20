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
    shapes = [Circle(), Square()]
    for shap in shapes:
        print(draw_shape(shap))


if __name__ == "__main__":
    start()
