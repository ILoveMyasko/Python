from figures_1 import Rectangle, Square, Shape

def test_shape_init():
    shape_1 = Shape(10,20)
    assert shape_1.x ==10
    assert shape_1.y ==20
    shape_2 = Shape(-10, 20.4)
    assert shape_2.x==-10
    assert shape_2.y== 20.4
def test_rectangle_init():
    rect = Rectangle(1,2,3,4)
    assert rect.width == 1 
    assert rect.height == 2 
    assert rect.x == 3 
    assert rect.y == 4
def test_rectangle_area():
    rect_1 = Rectangle(1, 5)

    assert rect_1.area == 5

    rect_2 = Rectangle(5, 0)
    assert rect_2.area == 0

    rect_3 = Rectangle(0, 5)
    assert rect_3.area == 0

def test_square_area():
    square_1 = Square(4)

    assert square_1.area == 16

    square_2 = Square(1)

    assert square_2.area == 1

    square_3 = Square(0)

    assert square_3.area == 0

def test_rect_modify_parameters():
    rect = Rectangle(2,3,4,5)

    assert rect.area == 6
    
    rect.width = 20
    assert rect.height == 3
    assert rect.area == 60

    rect.height = 5
    assert rect.width ==20
    assert rect.area == 100
def test_square_modify_parameters():
    square = Square(5)
    assert square.area == 25

    square.width = 2
    assert square.width== square.height
    assert square.area == 4

    square.height = 5
    assert square.width== square.height
    assert square.area == 25

def test_liskov_principle():
    def calcAreaForTrimmedRect(rect: Rectangle) -> int:
            rect.width = 4
            return rect.area
    rect = Rectangle(3, 3)
    square = Square(1)
    square.width = 4
    
    assert calcAreaForTrimmedRect(rect) ==  12
    assert calcAreaForTrimmedRect(square) == 16
