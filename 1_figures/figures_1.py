"""
Source code from our lectures.
class Shape:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Rectangle(Shape):
  def __init__(self, width, height, x=0, y=0):
    super().__init__(x, y)
    self.width = width
    self.height = height

class Square(Rectangle):
  def __init__(self, side, x=0, y=0):
    super().__init__(side, side, x, y)

What's wrong here? The problem lies in Square class, which uses Rectangle's constructor, which allows for width and height to have different values.
And this only works for rectangle, but not a square. We also basically don't store height and width for square, we only have side's length. 
So we also want to be able to get width and height for Square class.
What can we do to fix that?
We can you built-in properties (@property), which transforms an attribute into a property:
"""


class Shape:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Rectangle(Shape):
    def __init__(self, width, height, x=0, y=0):
        super().__init__(x, y)
        self.width = width
        self.height = height

    @property
    def area(self):
        return self.width * self.height
    
class Square(Rectangle):
    def __init__(self, side, x=0, y=0):
        super().__init__(side, side, x, y)

    @property
    def width(self):
        print("width prop")
        return self._width

    @width.setter
    def width(self, value):
        print("width setter")
        self._width = self._height = value

    @property
    def height(self):
        print("height prop")
        return self._height

    @height.setter
    def height(self, value):
        print("height setter")
        self._width = self._height = value

