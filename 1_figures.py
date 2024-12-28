
"""
Source code from our lectures.
class Rectangle(Shape):
  def __init__(self, width, height, x=0, y=0):
    super().__init__(x, y)
    self.width = width
    self.height = height

class Square(Rectangle):
  def __init__(self, side, x=0, y=0):
    super().__init__(side, side, x, y)

What's wrong here? The problem lies in Square class, which uses Rectangle's constructor, which allows for width and height to have different values.
And this only works for rectangle, but not a square.
What can we do to fix that?
We can you built-in properties (@property decorators), which transforms an attribute to a property:
"""


class Shape:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Rectangle(Shape):
    def __init__(self, width, height, x=0, y=0):
        super().__init__(x, y)
        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

class Square(Rectangle):
    def __init__(self, side, x=0, y=0):
        super().__init__(side, side, x, y)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
    #now we can be sure that width and height has the same value
        self._width = self._height = value

    @property
    def height(self):
        return self._height

    @height.setter
    #same if we change height
    def height(self, value):
        self._width = self._height = value

if __name__ == "__main__":
 shape = Shape(x=100, y=50)
 print(f"Shape: x={shape.x}, y={shape.y}")

 rectangle = Rectangle(width=50, height=100, x=0, y=0)
 print(f"Rectangle: x={rectangle.x}, y={rectangle.y}, width={rectangle.width}, height={rectangle.height}")

 square = Square(side=10, x=5, y=5)
 print(f"Square: x={square.x}, y={square.y}, width={square.width}, height={square.height}")

 # now lets change width and then height and check whether height and width respectively also changed.
 square.width = 20 
 print(f"Width increased to {square.width}, Square: width={square.width}, height={square.height}")

 square.height = 30
 print(f"Height increased to {square.height}, Square: width={square.width}, height={square.height}")