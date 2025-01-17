from figures_1 import Rectangle, Square


def test_rectangle_area():
    rect_1 = Rectangle(1, 5)

    assert rect_1.area() == 5

    rect_2 = Rectangle(5, 0)
    assert rect_2.area() == 0

    rect_3 = Rectangle(0, 5)
    assert rect_3.area() == 0

def test_square_area():
    square_1 = Square(4)

    assert square_1.area() == 16

    square_2 = Square(1)

    assert square_2.area() == 1

    square_3 = Square(0)

    assert square_3.area() == 0


def test_square_modify_parameters():
    square = Square(5)

    assert square.area == 25

    square.width = 2
    assert square.area == 4

    square.height = 5
    assert square.area == 25

def test_liskov_principle():
    rect = Rectangle(3, 3)
    square = Square(1)

    square.width = 4
    square.height = 5
    assert square.width == square.height
    square.width = 2
    square.height = 3
    assert rect.area() == square.area()